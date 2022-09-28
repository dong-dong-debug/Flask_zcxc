from sqlalchemy import Table
from common.database import dbconnect

dbsession, md, Dbase = dbconnect()


class Billcarry(Dbase):
    __table__ = Table('billcarry', md, autoload=True)

    # 插入一条查询记录
    def insert_billcarry(self, sourcepath, destpath, status=1):
        billcarry = Billcarry(sourcepath=sourcepath, destpath=destpath, status=status)
        dbsession.add(billcarry)
        dbsession.commit()

    # 修改一条查询记录
    def update_billcarry(self, status, sourcepath, destpath):
        bill = dbsession.query(Billcarry).filter_by(sourcepath=sourcepath, destpath=destpath,status=1).first()
        bill.status = status
        dbsession.commit()

    # 查询表单id
    def find_billcarryid(self, sourcepath, destpath):
        result = dbsession.query(Billcarry.id).filter(Billcarry.sourcepath == sourcepath,
                                                      Billcarry.destpath == destpath).all()
        return result

    # 根据状态查询表单
    def find_billcarry_by_status(self):
        result = dbsession.query(Billcarry.id).filter(Billcarry.status == 1).all()
        return result

    # 根据id查询表单
    def find_billcarry_by_id(self, id):
        result = dbsession.query(Billcarry.sourcepath, Billcarry.destpath).filter(Billcarry.id == id).all()
        return result

    # 根据源路径和目的路径查询表单状态
    def find_bill_by_source_and_dest(self, sourcepath, destpath):
        return dbsession.query(Billcarry).filter(Billcarry.sourcepath == sourcepath,
                                                 Billcarry.destpath == destpath, Billcarry.status == 1).first()

    # 查看是否存在已经运行的资源
    def find_bill_islive(self):
        return dbsession.query(Billcarry).filter(Billcarry.status == 1).count()
