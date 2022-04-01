from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

members = {} # id:member
altIds = {}  # altId:id

from rollcall import helper

app.config['DATA'] = helper.setupDirs()
helper.getAllMembers()