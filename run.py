# -*- coding:utf-8 -*-
from flask import Flask, render_template,redirect,jsonify,request
# from dbORM import db,User, Post
# import thumb
from moduleGlobal import app,cache
# from moduleGlobal import app, qiniu_store, QINIU_DOMAIN, TAG, UPLOAD_URL
# import moduleAdmin as admin
import flask_login
import requests


app.secret_key = '123456'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User( flask_login.UserMixin ):
    def __init__(self,id):
        self.id=id
@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/light')
@flask_login.login_required
def light():
    return render_template("light.html")
@app.route('/door')
# @flask_login.login_required
def door():
    return render_template("door/door.html")
@app.route('/desk')
# @flask_login.login_required
def desk():
    return render_template("door/desk.html")

###################APIS#######################
@app.route('/api/light', methods=['POST','GET'])
@flask_login.login_required
def lightApi():
    if request.method == 'POST':
        lightStatus = request.form['lightStatus']
        globalStatus = request.form['globalStatus']
        rawData=[float(globalStatus),float(lightStatus)]
        if lightStatus=="1":
            cache.set("LIGHT_1_U",rawData)
            print cache.get("LIGHT_1_U")

        else:
            cache.set("LIGHT_1_U", rawData)
            print cache.get("LIGHT_1_U")



    rawData = cache.get("LIGHT_1_D")

    return jsonify({'status':'on','data':rawData})

@app.route('/api/desk', methods=['POST','GET'])
# @flask_login.login_required
def deskApi():
    if request.method == 'POST':
        deskStatus = request.form['deskStatus']
        rawData=[float(deskStatus)]
        if deskStatus=="1":
            # cache.set("DESK_1_U",rawData)
            cache.lpush('Q', rawData)
            # print cache.get("DESK_1_U")

        else:
            cache.lpush('Q', rawData)
            # cache.set("DESK_1_U", rawData)
            # print cache.get("DESK_1_U")



    rawData = cache.get("DESK_1_D")

    return jsonify({'status':'on','data':rawData})

@app.route('/api/door', methods=['POST','GET'])
# @flask_login.login_required
def doorApi():

    if request.method == 'POST':

        doorStatus = request.form['doorStatus']
        globalStatus = request.form['globalStatus']
        dName = "DOOR_1"
        rawData=[dName,float(globalStatus),float(doorStatus)]
        print rawData
        if doorStatus=="1":
            cache.lpush('Q', rawData)
            # cache.set("DOOR_1_U",rawData)
            # print cache.get("DOOR_1_U")

        else:
            cache.lpush('Q', rawData)
            # cache.set("DOOR_1_U", rawData)
            # print cache.get("DOOR_1_U")



    rawData = cache.get("DOOR_1_D")

    return jsonify({'status':'on','data':rawData})

@app.route('/api/login', methods=['POST','GET'])
def loginApi():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        r = requests.get("http://128.1.67.182/api/verify?username=" + username + "&psswd=" + password)
        result = r.json()
        if result['status'] == "ok":
            # login
            user = User(int(result["content"]["uid"]))
            flask_login.login_user(user)
            # return redirect(url_for('protected'))
            return jsonify({"status": "ok", "msg": "登陆成功"})
        # TODO:other reasons
        else:
            return jsonify({"status": "failed", "msg": "登陆失败"})

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'



# @app.route('/api/test', methods=['POST','GET'])
# def testApi():
#     if request.method=='POST':
#         uid = request.form['uid']
#         name = request.form['name']
#         cache.delete('testData')
#         cache.set('testData',{"uid":uid,'name':name})

#         return jsonify({'status':'ok','content':{"uid":uid,'name':name}})
#     if   request.method == 'GET':
#         rv = cache.get('testData')
#         print 'get '
#         if rv is None:
#             return jsonify({'status': 'error'})
#         uid = rv['uid']
#         name = rv['name']
#         return jsonify({'status':'ok','content':{"uid":uid,'name':name}})


application = app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8085)
