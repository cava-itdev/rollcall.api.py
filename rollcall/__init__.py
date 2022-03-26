from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

members = {}

from rollcall import routes, helpers

helpers.setupDirs()
helpers.getMembers()