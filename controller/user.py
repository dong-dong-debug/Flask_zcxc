from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from module.user import Users

user = Blueprint("user", __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        user = Users()
        username = request.form.get('username')
        password = request.form.get('password')
        result = user.find_by_username(username)
        if len(result) == 1 and result[0].password == password:
            session['username'] = username
            return redirect(url_for("index.idx"))
        else:
            flash("邮箱和密码不匹配！")
            return redirect(url_for("user.login"))