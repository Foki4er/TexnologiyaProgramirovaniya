from flask import Flask
from flask_restful import Api
import sqlite3
import os

app = Flask(__name__, template_folder='Templates')
api = Api(app)
app.json.ensure_ascii = False
app.secret_key = os.urandom(24)
#подключение к БД
con = sqlite3.connect('exercise_service.db', check_same_thread=False)