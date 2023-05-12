from flask_pymongo import PyMongo
from flask import Flask
import pymongo
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')

conn = os.environ.get('MONGODB_CONN')
client = pymongo.MongoClient(conn, serverSelectionTimeoutMS=50000)
db = client.db


from application import routes
