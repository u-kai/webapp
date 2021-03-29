from flask import Blueprint, render_template,flash,redirect,url_for

applicant_app = Blueprint("applicant_app", __name__, template_folder="templates", static_folder="./statics")

@applicant_app.route("/")
def index():
    print("not dev yet")
    flash("not dev yet")
    return redirect(url_for("common_app.index"))
    # return render_template("applicant_app/index/html")

@applicant_app.route("/narrow_down")
def narrow_down():
    print("not dev yet")
    flash("not dev yet")
    return redirect(url_for("common_app.index"))