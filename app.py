from flask import Flask, g
from common import config
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY'] = os.urandom(24)  # 生成随机数种子，用于产生sessionID
# 实例化db对象
db = SQLAlchemy(app)

from controller.user import *
app.register_blueprint(user)

from controller.index import *
app.register_blueprint(index)

from module.user import Users
@app.before_request
def before_request():
    username = session.get("username")
    if username:
        try:
            user = Users.find_by_username(username)
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            # setattr(g,"user",user)
            g.user = user
        except:
            g.user = None


# 请求来了 -> before_request -> 视图函数 -> 视图函数中返回模板 -> context_processor

@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}



if __name__ == '__main__':
    app.run()
