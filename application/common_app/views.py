from flask import Blueprint, render_template

common_app = Blueprint("common_app", __name__, template_folder="./templates", static_folder="./static")

@common_app.route("/")
def index():
    return render_template("index.html")