import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import datetime
import json
to_json = {"data": []}



app = Flask(__name__)
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rjgrid@127.0.0.1:3306/littlebook'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
class books(db.Model):   #书籍表及各字段
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4','mysql_collate': 'utf8mb4_unicode_ci'}
    bkid = db.Column(db.Integer,primary_key=True,nullable=False,unique=True,autoincrement=True)
    bkclass = db.Column(db.Integer,nullable=True)
    bkname = db.Column(db.String(48),nullable=False,default="")
    bkauthor = db.Column(db.String(32),nullable=False,default="")
    bkpublisher = db.Column(db.String(16),default="NULL")
    bkfile = db.Column(db.String(256),nullable=False,default="")
    bkcover = db.Column(db.String(120),default="NULL")
    bkprice = db.Column(db.Integer,default=1)

class comment(db.Model):   #评论表及各字段
    __table_args__ = {'mysql_engine': 'InnoDB','mysql_charset': 'utf8mb4','mysql_collate': 'utf8mb4_unicode_ci'}
    cmid = db.Column(db.Integer,primary_key=True,nullable=False,unique=True,autoincrement=True)
    uid = db.Column(db.String(128),nullable=False,default="")
    uname = db.Column(db.String(48),nullable=False,default="")
    ccontent = db.Column(db.String(128),default="NULL")
    bkname = db.Column(db.String(16),nullable=False,default="")
    bkid = db.Column(db.Integer,nullable=False)
    uavatar = db.Column(db.String(256),nullable=False,default="")
    ctime = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)

class users(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB','mysql_charset': 'utf8mb4','mysql_collate': 'utf8mb4_unicode_ci'}
    id = db.Column(db.Integer,primary_key=True,nullable=False,unique=True,autoincrement=True)
    uid = db.Column(db.String(128),nullable=False,default="")
    uname = db.Column(db.String(40),default="")
    ugender = db.Column(db.Integer,default="")
    uaddress = db.Column(db.String(128),default="NULL")
    ubalance = db.Column(db.Integer,default="")
    uavatar = db.Column(db.String(256),default="NULL")
    skey = db.Column(db.String(128),nullable=False,default="")
    sessionkey = db.Column(db.String(128),nullable=False,default="")
    create_time = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)
    update_time = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now,onupdate=datetime.datetime.now)

class orders(db.Model):
    __table_args__ = {'mysql_engine': 'InnoDB','mysql_charset': 'utf8mb4','mysql_collate': 'utf8mb4_unicode_ci'}
    oid = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    uid = db.Column(db.String(128),nullable=False,default="")
    oprice = db.Column(db.Integer,default=0)
    otime = db.Column(db.DateTime,default=datetime.datetime.now)
    bkid = db.Column(db.Integer,nullable=False)





def select_books():   #查询书籍表所有信息
    msg = books.query.all()
    for i in msg:
        to_json["data"].append({"author": i.bkauthor,"cover_url": i.bkcover,"book_id": i.bkid,"book_name": i.bkname,\
                                "book_price": i.bkprice,"book_publisher": i.bkpublisher,"file_url": i.bkfile,"catego\
                                ry": i.bkclass})
    return to_json

def userlogin(**args):
    uid =args['uid']
    skey = args['skey']
    sessionkey = args['sessionkey']
    # uname = args['nickName']
    # ugender = args['gender']
    # uaddress = args['province']+ " . "+args['city']
    # uavatar = args['avatarUrl']
    usrmsg = users.query.filter_by(uid=uid).first()
    #print(sessionkey)
    if usrmsg is not None:
        print("updating")
        try:
            usrmsg.skey = skey
            usrmsg.sessionkey = sessionkey
            db.session.commit()
            print("updating done")
            return 0
        except Exception as e:
            return -2
            #updateuser = users
    print("creating")
    try:
        createuser = users(uid=uid,skey=skey,sessionkey=sessionkey)
        db.session.add(createuser)
        db.session.commit()
        print("creating done")
        return 0
    except Exception as e:
        print(e)
        return -1

def userupdate(**args):
    uname = args['uname']
    ugender = args['ugender']
    uavatar = args['uavatar']
    uaddress = args['city'] + " * "+ args['province']
    skey = args['skey']
    usrmsg = users.query.filter_by(skey=skey).first()
    if usrmsg is not None:
        try:
            usrmsg.uname = uname
            usrmsg.ugender = ugender
            usrmsg.uaddress = uaddress
            usrmsg.uavatar = uavatar
            db.session.commit()
            #usrmsg = users.query.filter_by(skey=skey).first()
            #print(json.dumps(json.loads(usrmsg)))
            return json.dumps({"status": 0,"ubalance": usrmsg.ubalance})
        except Exception as e:
            return json.dumps({'status': 1,"errmsg": "userinfo update fail"})



