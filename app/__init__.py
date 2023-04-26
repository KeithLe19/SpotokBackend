from flask import Flask
from flask_cors import CORS
from app.persistence import persistence
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)
persistence.establish_connection()

from app.routes import index_route, auth_route, spotify_route





