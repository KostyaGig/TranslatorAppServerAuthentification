import json
import string
import random

from flask import Flask, jsonify, request
from deep_translator import GoogleTranslator
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
db = SQLAlchemy(app)

# region translate logic
TRANSLATED_SUCCESS_MARK = "Success"
TRANSLATED_FAILURE_MARK = "Failure"

RU_LANGUAGE = "ru"
EN_LANGUAGE = "en"

@app.route('/translate/<string:src_word>')
def translate(src_word):
    try:
        if isEmpty(src_word):
            return responseAsJson("Field not will be empty", TRANSLATED_FAILURE_MARK, "", "", "", "")
        else:
            translator_word = GoogleTranslator(source='auto', target='en').translate(src_word)
            return responseAsJson("", TRANSLATED_SUCCESS_MARK, RU_LANGUAGE, EN_LANGUAGE, src_word, translator_word)
    except Exception as e:
        if isEmpty(src_word):
            return responseAsJson("Field not will be empty", TRANSLATED_FAILURE_MARK, "", "", "", "")
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
        return responseAsJson("Not correctly entered word", TRANSLATED_FAILURE_MARK, "", "", "", "")
    else:
        return responseAsJson("Cannot be translated", TRANSLATED_FAILURE_MARK, "", "", "", "")
# endregion

# region db model
class Employee(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    user_unique_key = db.Column(db.String(100), unique=True)
    user_name = db.Column(db.String(20), unique=False)
    number_phone = db.Column(db.String(20), unique=True)
    words = db.relationship('Word', backref='owner', lazy=True)

    def __init__(self, user_unique_key, user_name, number_phone):
        self.user_name = user_name
        self.user_unique_key = user_unique_key
        self.number_phone = number_phone

    def __repr__(self):
        return '<User %r>' % self.username

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    src = db.Column(db.String(100), unique=False)
    translated = db.Column(db.String(100), unique=False)
# endregion

# region auth
@app.route('/')
def index():
    return "default page"

@app.route('/login/<string:unique_key>')
def login_by_unique_key(unique_key):
    try:
        db.create_all()
        db.session.commit()
        if Employee.query.filter_by(user_unique_key=unique_key).count() >= 1:
            return "Success login to account!"
        else:
            return "You not registered in system yet!"
    except Exception as e:
        return "Login user happened error: " + str(e)


USER_NAME_KEY = 'userName'
NUMBER_PHONE_KEY = 'userNumberPhone'

REGISTER_SUCCESS_MARK = "Success"
REGISTER_FAILURE_MARK = "Failure"
REGISTER_EXIST_MARK = "Exist"

@app.route('/register', methods=['POST'])
def register():
    try:
        db.create_all()
        db.session.commit()
        user_name = request.args.get(USER_NAME_KEY)
        user_number_phone = request.args.get(NUMBER_PHONE_KEY)
        if isEmpty(user_name) or isEmpty(user_number_phone):
            return jsonify({
                "message": "Field not will be empty",
                "mark": REGISTER_FAILURE_MARK,
                "uniqueKey": ""
            })
        else:
            if db.session.query(Employee).filter_by(number_phone=user_number_phone).count() < 1:
                unique_key = generate_unique_key()
                user = Employee(user_unique_key=unique_key, user_name=user_name, number_phone=user_number_phone)
                db.session.add(user)
                db.session.commit()
                return jsonify({
                    "message": "Success register user in system",
                    "mark": REGISTER_SUCCESS_MARK,
                    "uniqueKey": unique_key
                })
            else:
                return jsonify({
                    "message": "User with number phone" + user_number_phone + " already exist!",
                    "mark": REGISTER_EXIST_MARK,
                    "uniqueKey": ""
                })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Register user happened error " + str(e),
            "mark": REGISTER_FAILURE_MARK,
            "uniqueKey": ""
        })


LOGIN_SUCCESS_MARK = "Success"
LOGIN_FAILURE_MARK = "Failure"

@app.route('/login', methods=['POST'])
def login_by_number_phone_and_password():
    try:
        db.create_all()
        db.session.commit()
        user_name = request.args.get(USER_NAME_KEY)
        user_number_phone = request.args.get(NUMBER_PHONE_KEY)
        if isEmpty(user_name) or isEmpty(user_number_phone):
            return jsonify({
                "message": "Field not will be empty",
                "mark": LOGIN_FAILURE_MARK,
                "uniqueKey": ""
            })
        else:
            if db.session.query(Employee).filter_by(number_phone=user_number_phone).count() < 1:
                return jsonify({
                    "message": "User with number " + user_number_phone + " not found!",
                    "mark": LOGIN_FAILURE_MARK,
                    "uniqueKey": ""
                })
            else:
                user = Employee.query.filter_by(number_phone=user_number_phone).one()
                if user.user_name != user_name or user.number_phone != user_number_phone:
                    return jsonify({
                        "message": "Incorrect name user for number " + user.number_phone,
                        "mark": LOGIN_FAILURE_MARK,
                        "uniqueKey": ""
                    })
                else:
                    return jsonify({
                        "message": "Success login in system!",
                        "mark": LOGIN_SUCCESS_MARK,
                        "uniqueKey": user.user_unique_key
                    })
    except Exception as e:
        return jsonify({
            "message": "Login by number and phone happened error " + str(e),
            "mark": LOGIN_FAILURE_MARK,
            "uniqueKey": ""
        })

def generate_unique_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
# endregion

# region user communication

USER_UNIQUE_KEY = 'userUniqueKey'
# translate word if user was authorize in system
@app.route('/translateUniqueKey/<string:src_word>', methods=['POST'])
def translateWithAuthorizeInSystem(src_word):
    try:
        user_unique_key = request.args.get(USER_UNIQUE_KEY)
        if db.session.query(Employee).filter_by(user_unique_key=user_unique_key).count() < 1:
            # translate without added word in db
            # reuse method for translate word
            return translate(src_word)
        else:
            user = Employee.query.filter_by(user_unique_key=user_unique_key).one()
            translated_word = GoogleTranslator(source='auto', target='en').translate(src_word)

            user_words = user.words
            if len(user_words) <= 0:
                # add word to db
                word = Word(src=src_word,translated=translated_word,owner=user)
                insert_word(word)
                return "Word " + src_word + " was success inserted in this user"
            else:
                user_src_words = list()
                for user_word in user_words:
                    print(user_word.src)
                    # add only src word
                    user_src_words.append(user_word.src)

                # check on unique word
                if src_word in user_src_words:
                    return "Word " + src_word + " already exist in this user"
                else:
                    # add word to db
                    word = Word(src=src_word, translated=translated_word, owner=user)
                    insert_word(word)
                    return "Word " + src_word + " while not exist in this user"

    except Exception as e:
        return "TranslateWithUniqueUserKey: " + str(e)

def insert_word(word):
    db.session.add(word)
    db.session.commit()

class UserWord:
    def __init__(self, src, translated):
        self.src = src
        self.translated = translated

    def serialize(self):
        return {
            'src': self.src,
            'translated': self.translated
        }
# all users
@app.route('/users')
def users():
    users = Employee.query.all()
    users_name = list()
    for user in users:
        users_name.append(user.user_name)
    return jsonify(names=users_name) # {"names":["Kostya","Egor"]}

# all words user
@app.route('/users/<string:user_name>/words')
def words_user(user_name):
    user = Employee.query.filter_by(user_name=user_name).one()
    words = user.words
    user_words = []
    for word in words:
        user_word = UserWord(word.src,word.translated)
        user_words.append(user_word.serialize())
    return jsonify(user_words=user_words) #{"user_words":[{"src":"\u041b\u0430\u043c\u043e\u0434\u0430","translated":"Lamoda"},{"src":"\u041b\u0430\u043c\u043e\u0434\u0430","translated":"Lamoda"},{"src":"\u041b\u0430\u043c\u043e\u0434\u0430","translated":"Lamoda"}]}

# for test Add test user
@app.route('/addUserForTest')
def addUserForTest():
    try:
        db.create_all()
        db.session.commit()
        user = Employee(user_unique_key="123", user_name="Kostya", number_phone="123")
        db.session.add(user)
        db.session.commit()
        return "Success add user for test"
    except Exception as e:
        return "Add user for test error: " + str(e)

# for test Add word by name user
@app.route('/addWordByName')
def add_words_by_user_name():
    try:
        user = Employee.query.filter_by(user_name='Kostya').one()
        word = Word(src='Ламода', translated='Lamoda', owner=user)
        insert_word(word)
        return ""
    except Exception as e:
        return "Add word by name error: " + str(e)

# for test
@app.route('/delete')
def clear_db():
    try:
        Employee.query.delete()
        db.session.commit()
        return "Db was cleared"
    except Exception as e:
        return "Delete db error " + str(e)

    # for test
    @app.route('/addUser')
    def add_user():
        db.create_all()
        db.session.commit()
        user = Employee(user_unique_key="1234", user_name="Egor", number_phone="1234")
        db.session.add(user)
        db.session.commit()
        added_user = Employee.query.filter_by(number_phone='1234').one()
        return 'Read added user here name ' + added_user.user_name

    # for test
    @app.route('/addWordUser')
    def add_word_user():
        added_user = Employee.query.filter_by(number_phone='123').one()
        word = Word(src='Мышь', translated='Mouse', owner=added_user)
        db.session.add(word)
        db.session.commit()
        return "ok"

    # for test
    @app.route('/userWords')
    def read_user_words():
        added_user = Employee.query.filter_by(number_phone='123').one()
        print(added_user.words)
        return str(added_user.words[-1].translated)

#endregion

if __name__ == "__main__":
    app.run()
