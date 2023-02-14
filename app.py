from flask import Flask, request, abort, url_for
from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Text

app = Flask(__name__)
# 数据库地址
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy()
db.init_app(app)


# 消息表
class Messages(db.Model):
    __tablename__ = 'messages'
    messageID = Column(String(200), primary_key=True)
    message = Column(Text())


# 请求记录表
class RequestRecords(db.Model):
    __tablename__ = 'requestRecords'
    requestKey = Column(String(200), primary_key=True)
    requestNumber = Column(Integer())


# 每个ip每天最大的请求次数
maximumRequests = 100
# uuidNamespace 可换可不换
uuidNamespace = 'eb357af3-db14-4a5d-af95-a92ea0779a51'


# 数据库初始化
@app.before_first_request
def before_first_request():
    db.create_all()


# ip访问限制
@app.before_request
def before_request():
    requestKey = "^".join([str(i) for i in [datetime.now().date(), request.remote_addr]])
    data = RequestRecords.query.get(requestKey)
    if data:
        # 访问次数+1
        data.requestNumber = data.requestNumber + 1
        db.session.commit()
        if data.requestNumber > maximumRequests:
            abort(406)
    else:
        # 某ip当日第一次访问
        requestRecord = RequestRecords(requestKey=requestKey, requestNumber=1)
        db.session.add(requestRecord)
        db.session.commit()


@app.errorhandler(404)
def error404(error):
    return "该链接无效！", 404


@app.errorhandler(405)
def error405(error):
    return "提交的数据为空！", 405


@app.errorhandler(406)
def error406(error):
    return "本日访问次数已用完，请明日再试！", 406


# 获取提交的信息并销毁
@app.get('/<int:messageID>')
def getMessage(messageID):
    messageID = str(messageID)
    message = Messages.query.get_or_404(messageID)
    # 删除数据
    db.session.delete(message)
    db.session.commit()
    return f"{message.message}"


# 接收上传的信息
@app.post('/addMessage')
def addMessage():
    message = request.form.get("message")
    if not message:
        abort(405)
    # 根据message的生成一个uuid
    messageID = f"{uuid.uuid4().int}{uuid.uuid5(uuid.UUID(uuidNamespace), message).int}"
    message = Messages(messageID=messageID, message=message)
    db.session.add(message)
    db.session.commit()
    return url_for("addMessage", _external=True).replace("addMessage", messageID)


@app.get("/")
def index():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form action="/addMessage" method="post">
        分享的数据: <input type="text" name="message"><input type="submit"><br>
</form>
</body>
</html>"""
    return html
