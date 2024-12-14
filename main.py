from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# import forms
from forms import *
# import tables
from tables import *
# import database
from db import db

import os
from dotenv import load_dotenv


load_dotenv()


### ------------------------------ MAIN CLASS ------------------------------ ###
class RiceWebApp:

    ### ------------------------------ !!!CONSTRUCTOR!!! ------------------------------ ###
    def __init__(self):
        # Configure Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY')
        self.register_routes()

        # Configure database
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
        db.init_app(self.app)

        # Configure Flask-Login
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        @self.login_manager.user_loader
        def load_user(user_id):
            return db.get_or_404(User, user_id)

        # Handle order completion
        self.current_order_id = 1
        self.order_completed = True


    ### -------------------------------- !!!ROUTES!!! --------------------------------- ###
    def register_routes(self):
        # ---------- MAIN <page> ---------- #
        @self.app.route('/', methods=['POST', 'GET'])
        def main():
            if request.method == 'POST':
                action = request.form.get('action')
                if action == 'send-feedback':
                    self.get_feedback()

            return render_template("index.html", page_name="main")

        # ---------- REGISTER <page> ---------- #
        @self.app.route('/register', methods=["GET", "POST"])
        def register():
            form = RegisterForm()

            # Check the method is POST
            if request.method == "POST":
                action = request.form.get('action')
                # Conditions for all buttons
                if action == "send-feedback":
                    return self.get_feedback()
                elif action == "register":
                    if form.validate_on_submit():  # Check if the form passes all validations
                        return self.registrate_new_user(form)

            return render_template('register.html', form=form, page_name='register')

        # ---------- LOGIN <page> ---------- #
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            # Login form
            login_form = LoginForm()
            # validation check of login form
            if login_form.validate_on_submit():
                # user object condition to match user input
                result = db.session.execute(db.select(User).where(User.email == login_form.email.data))
                user = result.scalar()

                # conditions if user does not exist/password does not match
                if not user:
                    flash("Unday pochta mavjud emas!", "email_error")
                    return redirect(url_for('login'))
                elif not check_password_hash(user.password, login_form.password.data):
                    flash("Parol noto'g'ri!", "password_error")
                    return redirect(url_for('login'))
                else:
                    login_user(user)
                    return redirect(url_for('order'))

            return render_template('login.html', form=login_form, page_name='login')

        # ---------- LOGOUT <page> ---------- #
        @self.app.route('/logout')
        def logout():
            logout_user()
            return redirect(url_for('login'))

        # ---------- ORDER <page> ---------- #
        @self.app.route('/buyurtma-berish', methods=["GET", "POST"])
        def order():
            if request.method == 'POST':
                if current_user.is_authenticated:
                    action_value = request.form.get('action')
                    if action_value == 'send-feedback':
                        self.get_feedback()
                    else:
                        # Check if product exists, if not add that product
                        product_result = db.session.execute(
                            db.select(Product)
                            .where(Product.name == action_value.capitalize())
                        ).scalar()

                        if not product_result:
                            product = Product(name=action_value.capitalize())
                            db.session.add(product)
                            db.session.commit()


                        # Check if the order completed, if yes add new order
                        current_order = db.session.execute(
                            db.select(Order).where(Order.user_id == current_user.id).order_by(Order.id.desc())
                        ).scalar()

                        # Check if there is no orders yet
                        if not current_order:
                            current_order = Order(user=current_user)
                            db.session.add(current_order)
                            db.session.commit()
                        else:
                            # If order is there, check for order completion
                            if current_order.order_complete:
                                current_order = Order(user=current_user)
                                db.session.add(current_order)
                                db.session.commit()

                        # Adding order_details to the database
                        self.current_order_id = db.session.execute(
                            db.select(Order.id)
                            .where(Order == current_order)
                        ).scalar()
                        current_product = db.session.execute(
                            db.select(Product)
                            .where(Product.name == action_value.capitalize())
                        ).scalar()

                        product_quantity = request.form.get('quantity')
                        new_order_details = OrderDetails(
                            order=current_order,
                            product=current_product,
                            quantity=product_quantity
                        )
                        db.session.add(new_order_details)
                        db.session.commit()

                # if user is not logged in showing flash message
                else:
                    flash("Buyurtma berish uchun ro'yxatdan o'ting yoki akkauntga kiring!", "error")
                    return redirect(url_for('order'))

            return render_template("order.html", page_name="order")

        # My orders <route> #
        @self.app.route("/buyurtmalarim", methods=["GET", "POST"])
        def my_orders():
            if request.method == "POST":
                action = request.form.get('action')
                if action == 'send-feedback':
                    self.get_feedback()
            if current_user.is_authenticated:
                user_orders = db.session.execute(
                    db.select(Order).where(Order.user_id == current_user.id)
                ).scalars().all()

                return render_template("my-orders.html", user_orders=user_orders, page_name="my_orders")

            return render_template("my-orders.html", page_name="my_orders")

        @self.app.route("/buyurtma-<int:order_id>", methods=["GET", "POST"])
        def my_order(order_id):
            this_order = db.session.get(Order, order_id)
            if request.method == "POST":
                action = request.form.get('action')
                if action == "complete-order":
                    # Complete the order
                    this_order.order_complete = True
                    db.session.commit()

                    return redirect(url_for('my_orders'))

            order_details = db.session.execute(
                db.select(OrderDetails)
                .where(OrderDetails.order_id == order_id)
            ).scalars().all()

            products = db.session.execute(db.select(Product)).scalars().all()


            return render_template("my-order.html",
                                   order_details=order_details,
                                   products=products,
                                   order_id=order_id,
                                   this_order=this_order
                                   )

    ### ------------------------------ !!!FUNCTIONS NEEDED!!! ------------------------------ ###
    # ---------- Get feedback <method> ---------- #
    def get_feedback(self):
        # Feedback from user (new data to the table <user_feedback>)
        new_feedback = UserFeedback(
            name=request.form.get('name'),
            phone=request.form.get('phone_number'),
            feedback=request.form.get('feedback')
        )
        # Save to the database
        db.session.add(new_feedback)
        db.session.commit()

        flash("Izohingiz qabul qilindi! E'tibor uchun tashakkur!", "success")

    # ---------- Register new user <method> ---------- #
    def registrate_new_user(self, form):
        # Data from registrate Form
        name = form.name.data
        hashed_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        # New User object (for <users> table)
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
        )
        # Save to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('order'))

    # ---------- Run Application <method> ---------- #
    def run_app(self, debug=True, port=5050, host='127.0.0.1'):
        self.app.run(debug=debug, port=port, host=host)


if __name__ == '__main__':
    app = RiceWebApp()
    with app.app.app_context():
        db.create_all()

    app.run_app(debug=True)












