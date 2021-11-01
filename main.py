import string
import random

from flask import Flask, jsonify, request
from deep_translator import GoogleTranslator
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_unique_key = db.Column(db.String(100), unique=True)
    user_name = db.Column(db.String(20), unique=False)
    number_phone = db.Column(db.String(20), unique=True)

    def __init__(self, user_unique_key, user_name, number_phone):
        self.user_name = user_name
        self.user_unique_key = user_unique_key
        self.number_phone = number_phone

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    return "default page"

@app.route('/login/<string:user_unique_key>')
def login_by_unique_key(user_unique_key):
    try:
        db.create_all()
        db.session.commit()
        if db.session.query(Employee).filter_by(user_unique_key=user_unique_key).count() > 1:
            return "Success login to account!"
        else:
            return "You not registered in system yet!"
    except Exception as e:
        return "Login user happened error: " + e.message


USER_NAME_KEY = 'user_name'
NUMBER_PHONE_KEY = 'user_number_phone'

@app.route('/login', methods=['POST'])
def login_by_number_phone_and_password():
    try:
        user_name = request.form[USER_NAME_KEY]
        user_number_phone = request.form[NUMBER_PHONE_KEY]
        if db.session.query(Employee).filter_by(number_phone=user_number_phone).count() < 1:
            return "User with number " + user_number_phone + " not found!"
        else:
            if db.session.query(Employee).filter_by(user_name=user_name).count() < 1:
                return "Incorrect number or name user"
            else:
                users = db.session.query(Employee)
                user = users.filter(number_phone=user_number_phone).one()
                return "Success login by number and phone, your unique key " + user.user_unique_key
    except Exception as e:
        return "Login user by number and phone happened error " + e.message

@app.route('/register', methods=['POST'])
def register():
    try:
        user_name = request.form[USER_NAME_KEY]
        user_number_phone = request.form[NUMBER_PHONE_KEY]
        if db.session.query(Employee).filter_by(number_phone=user_number_phone).count() < 1:
            unique_user_id = generate_unique_key()
            user = Employee(user_unique_key=unique_user_id, user_name=user_name, number_phone=user_number_phone)
            db.session.add(user)
            db.session.commit()
            return "Success register user in system!"
        else:
            return "User with number phone" + user_number_phone + ' already exist!'
    except Exception as e:
        db.session.rollback()
        return "Register user happened error " + e.message


def generate_unique_key():
    ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

SUCCESS_MARK = "Success"
FAILURE_MARK = "Failure"

RU_LANGUAGE = "ru"
EN_LANGUAGE = "en"

@app.route('/translate/<string:src_word>')
def translate(src_word):
    try:
        if isEmpty(src_word):
            return responseAsJson("Field not will be empty", FAILURE_MARK, "", "", "", "")
        else:
            translator_word = GoogleTranslator(source='auto', target='en').translate(src_word)
            return responseAsJson("", SUCCESS_MARK, RU_LANGUAGE, EN_LANGUAGE, src_word, translator_word)
    except Exception as e:
        if isEmpty(src_word):
            return responseAsJson("Field not will be empty", FAILURE_MARK, "", "", "", "")
        else:
            errorMessage = e.message
            return responseByErrorMessage(errorMessage)


def isEmpty(src):
    if src == "\"\"":
        return True
    else:
        return False


def responseAsJson(message, mark, fromLanguage, toLanguage, srcWord, translatorWord):
    return jsonify({
        "message": message,
        "mark": mark,
        "fromLanguage": fromLanguage,
        "toLanguage": toLanguage,
        "srcWord": srcWord,
        "translatorWord": translatorWord
    })


def responseByErrorMessage(message):
    if message == "text must be a valid text with maximum 5000 character, otherwise it cannot be translated":
        return responseAsJson("Not correctly entered word", FAILURE_MARK, "", "", "", "")
    else:
        return responseAsJson("Cannot be translated", FAILURE_MARK, "", "", "", "")


if __name__ == "__main__":
    app.run()
