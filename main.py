from flask import Flask, render_template
from app.config import Config
import os

app = Flask(__name__, template_folder="app/views", static_folder="static")


@app.route("/")
def home():
    return render_template("home.html")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.controllers import main as main_controller

    app.register_blueprint(main_controller)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
