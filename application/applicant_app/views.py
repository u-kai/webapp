from flask import Blueprint, render_template

applicant_app = Blueprint("applicant_app", __name__, template_folder="templates", static_folder="./statics")

@applicant_app.route("/")
def index():
    return render_template("applicant_app/index/html")