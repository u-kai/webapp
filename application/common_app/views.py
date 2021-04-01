from flask import Blueprint, render_template,flash,jsonify,request,redirect,url_for
import json
common_app = Blueprint("common_app", __name__, template_folder="./templates", static_folder="./static")

@common_app.route("/")
def index():
    return render_template("index.html")

@common_app.route("/enter_test")
def enter_test():
    return render_template("testscript.html")

@common_app.route("/test",methods=["POST"])
def test():
    where_query = "WHERE"
    posted_data = dict(request.form)
    for key in posted_data.keys():
        for value in request.form.getlist(key):
            where_query += f" {key} = {value} OR"
        where_query = where_query[:-3] + " AND"
    where_query = where_query[:-3]
    print(where_query)
        
    # print(request.form.getlist("test"))
    # data = dict(request.form)
    # print(data)
    # for key, value in request.form.items():
    #     print(key, value)
    print("sendpage")
    return redirect(url_for("common_app.index"))#jsonify({"body":request.json})