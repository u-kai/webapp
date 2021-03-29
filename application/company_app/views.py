from flask import Blueprint, render_template, request, redirect, jsonify, url_for, flash, session
from QueryFunctions import TableOperationBySQL
from config import Config
from Salt import salt
import hashlib
import random
from add_quote import add_single_quote
from datetime import timedelta
from functools import wraps

company_app = Blueprint("company_app", __name__, template_folder="templates", static_folder="./statics")
certifications_table = "companies_certifications"
conditions_table = "companies_conditions_test"

def login_required(company_app):
    @wraps(company_app)
    def inner(*args, **kwargs):
        if session.get("company_id") == False:
            return redirect(url_for("/login"))
        return company_app(*args, **kwargs)
    return inner

@company_app.route("/login",methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        print("!!!!!!!!!!!!!!!!!")
        table_operater = TableOperationBySQL(Config=Config, table_name=certifications_table)
        company_name = add_single_quote(request.form["company_name"])
        origin_password = request.form["company_password"] + salt
        hash_password = add_single_quote(hashlib.sha256((origin_password).encode('utf-8')).hexdigest())
        company_id = int(request.form["company_id"])
        select_datas = ["company_id","company_name","company_password"]
        condition_dict = {"company_id":company_id,
                        "company_name":company_name,
                        "company_password":hash_password}
        result = table_operater.select(select_datas, condition_dict)
        if result:
            session.permanent = True
            company_app.permanent_session_lifetime = timedelta(minutes=60)
            session["company_id"] = company_id
            print("success" ,session.get("company_id"))
            return redirect(url_for("company_app.enter_company_top"))
        else:
            flash("登録情報と一致しません")
            print("登録情報と一致しません")
    return render_template("company_app/login.html")

@company_app.route("/logout")
def logout():
    session.pop('company_id', None)
    print("logout")
    flash("ログアウトしました")
    return redirect(url_for("/"))


@company_app.route("/enter_new_regist")
def enter_new_regist():
    return render_template("company_app/new_regist.html")

@company_app.route("/new_regist",methods=["POST"])
def new_regist():
    origin_password = request.form["company_password"] + salt
    hash_password = add_single_quote(hashlib.sha256((origin_password).encode('utf-8')).hexdigest())
    company_name = add_single_quote(request.form["company_name"])
    ###Generate company_id range(100000000~199999999)
    company_id = random.randint(100000000, 199999999)
    table_operater = TableOperationBySQL(Config=Config, table_name=certifications_table)
    ###Confirm what company_id is only one
    ###
    condition_dict = {"company_id":company_id,
                      "company_name":company_name,
                      "company_password":hash_password}
    
    table_operater.insert(condition_dict)
    flash('新規登録ありがとうございます')
    return render_template("company_app/confirm_id.html",company_id=company_id)

@company_app.route("/enter_company_top")
@login_required
def enter_company_top():
    table_operater = TableOperationBySQL(Config=Config, table_name=conditions_table)
    select_datas = "*"
    condition_dict = {"company_id":session.get("company_id")}
    result = table_operater.select(select_datas, condition_dict)
    if result == ():
        print("データがありません。データを登録してください")
        return redirect(url_for("company_app.regist_new_conditions"))
    return render_template("company_app/company_top.html",result=next(iter(result)),company_id=session.get("company_id"))

@company_app.route("/regist_new_conditions",methods=["GET","POST"])
@login_required
def regist_new_conditions():
    if request.method == "POST":
        company_id = session.get("company_id")
        company_name = add_single_quote(request.form["company_name"])
        company_message = add_single_quote(request.form["company_message"])
        working_time = add_single_quote(request.form["working_time"])
        table_operater = TableOperationBySQL(Config=Config, table_name=conditions_table)
        condition_dict = {"company_id":company_id,
                        "company_name":company_name,
                        "company_message":company_message,
                        "working_time":working_time}
        table_operater.insert(condition_dict)
        print("insert is succsess")
        return redirect(url_for("company_app.enter_company_top"))
    else:
        return render_template("company_app/regist_new_conditions.html")

@company_app.route("/edit",methods=["POST"])
@login_required
def edit():
    company_id = session.get("company_id")
    company_name = add_single_quote(request.form["company_name"])
    company_message = add_single_quote(request.form["company_message"])
    working_time = add_single_quote(request.form["working_time"])
    where_data = {"company_id":company_id}
    update_data = {"company_name":company_name,
                    "company_message":company_message,
                    "working_time":working_time}
    table_operater = TableOperationBySQL(Config=Config, table_name=conditions_table)
    table_operater.update(where_data, update_data)
    print("内容を変更いたしました")
    return redirect(url_for("company_app.enter_company_top"))


@company_app.route("/delete",methods=["POST"])
@login_required
def delete():
    table_operater = TableOperationBySQL(Config=Config, table_name=conditions_table)
    identificate_data = {"company_id": int(session.get("company_id"))}
    table_operater.delete(identificate_data)
    print("delete is success")
    return redirect(url_for("company_app.enter_company_top"))