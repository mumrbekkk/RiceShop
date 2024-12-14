# English & Uzbek

----------------------------
EN
# Rice Shop Web Application (with Flask [Python])

## Description 
This is a simple Flask web application that includes many flask structured back end code manipulation, 
but with minimalistic front end usage. The case is not real but imaginatively built for selling products,
precisely rice.
----------------------------


UZ
# Guruch Do'konning Web Sayti (Flask [Python])

## Web sayt haqida
Bu oddiy Flask veb-ilovasi bo'lib, u ko'plab flask frameworkining back end ko'dini o'z ichiga oladi, 
lekin front end kodi minimalistik usulda yozilgan. Loiha haqiqiy emas, lekin mahsulotlarni, aniqroq qilib aytganda 
asosan guruch sotish uchun o'ylab chiqilgan xolos.
----------------------------

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/username/repository.git
   ```
2. Navigate to the project directory:
   ```bash
   cd repository
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file and add the following:
     ```plaintext
     APP_SECRET_KEY=your_secret_key
     SQLALCHEMY_DATABASE_URI=your_database_uri
     ```
5. Run the application:
   ```bash
   flask run
   ```


## Usage
1. Start the server:
   ```bash
   flask run
   ```
2. Open your browser and go to:
   ```
   http://127.0.0.1:5050
   ```
3. Log in or create an account to start managing tasks.


## Configuration
The application requires the following environment variables to be set:

- `APP_SECRET_KEY`: The secret key for Flask sessions.
- `SQLALCHEMY_DATABASE_URI`: The database connection string.

Create a `.env` file in the root directory with these variables:
