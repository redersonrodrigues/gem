from flask import Flask

app = Flask(__name__)

from app import controllers, models, views

# Additional application setup code can be added here if needed.
