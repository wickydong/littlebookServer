from flask import Flask
from flask import request
import requests
import test
import json
import hashlib
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rjgrid@127.0.0.1:3306/littlebook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
appid = "wx4e21bec3f41f537a"
secret = "1072f67c8b1ab136ea58cc856a1703a1"

# msg = {"data": [{"book_name": "茶馆","author": "老舍","book_publisher": "人民日报出报社","cover_url":\
#     "https://upload.12xue.com/14920682048.png"},{"book_name":"长夜漫漫路迢迢","author": "尤金·奥尼尔","book_publisher":\
#     "美国环球出版社","cover_url":"https://upload.12xue.com/14920682048.png"},{"book_name":"玩偶之家","author":\
#     "易卜生","book_publisher":"大英博物出版社","cover_url":"https://upload.12xue.com/14920682048.png"}],"result":0}
test.db.init_app(app)

@app.route('/getbook')
def getbook():
    want = request.args.get('want')
    if want == '1':
        msg = test.select_books()
        msg["result"] = 0
        return json.dumps(msg)


@app.route('/login')
def login():
    code = request.args.get("code")
    # rawdata = request.args.get("rawdata")
    # signature = request.args.get("signature")
    # encrypteddata = request.args.get("encrypteddata")
    # iv = request.args.get("iv")
    if code == None:
        return json.dumps({"status": 1,"errmsg": "参数缺失"})
    # rawdata = json.loads(rawdata)
    codemsg = {"appid": appid,"secret": secret,"js_code": code,"grant_type": "authorization_code"}
    code2session = requests.get("https://api.weixin.qq.com/sns/jscode2session",params=codemsg).json()
    # session_key = code2session['session_key']
    if "errmsg" in code2session:
        return json.dumps({"status": 2,"errmsg": "请求微信失败"})
    session_key = code2session['session_key']
    openid = code2session['openid']
    skey = hashlib.md5(session_key.encode('utf8')).hexdigest()
    userloginmsg = {'sessionkey': session_key,'uid': openid,'skey': skey}
    #user information insert SQL
    userlogin = test.userlogin(**userloginmsg)
    if userlogin == 0:
        return json.dumps({"status": 0,"errmsg": "请求成功","skey": skey})
    return json.dumps({"status": 3,"errmsg":"数据库操作失败"})


@app.route("/userinfo")
def userinfo():
    uname = request.args.get('nickName')
    ugender = request.args.get('gender')
    city = request.args.get('city')
    province = request.args.get('province')
    uavatar = request.args.get('avatarUrl')
    skey = request.args.get('skey')
    if skey is None:
        return json.dumps({"status": 1,"errmsg": "skey not found"})
    usrmsg = {'uname': uname,'ugender': ugender,'city': city,'province': province,'uavatar': uavatar,'skey': skey}
    userupdate = test.userupdate(**usrmsg)
    return userupdate




if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80,debug='true')
