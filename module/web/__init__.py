from flask import Flask
from config import Web

app = Flask(__name__)

app.run(port=Web.port)
