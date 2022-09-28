from sqlalchemy import Table
from common.database import dbconnect

dbsession, md, Dbase = dbconnect()


class Users(Dbase):
    __table__ = Table('users', md, autoload=True)

    # 根据用户名查找密码
    def find_by_username(self, username):
        result = dbsession.query(Users).filter_by(username=username).all()
        return result
