from flask import Flask, render_template, request, jsonify, redirect, url_for
from random import *

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

# 은솔님 DB
client = MongoClient('mongodb+srv://test:sparta@cluster0.ffudy0q.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.coffeeduckhu

# 이상훈 DB
# client = MongoClient('mongodb+srv://test:sparta@cluster0.xevhlvh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
# db = client.dbsparta


# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


#################################
##  HTML을 주는 부분             ##
#################################

@app.route('/')
def home():
    result = []
    for i in range(8):
        j = randint(1, 342)
        test = db.coffee.find_one({'coffee_id': j})
        url = test['coffee_image']
        result.append(url)

    token_receive = request.cookies.get('mytoken')
    try:
        print(result)
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"], variable=result)
    except jwt.ExpiredSignatureError:
        return render_template('index.html', variable=result)
    except jwt.exceptions.DecodeError:
        return render_template('index.html', variable=result)

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/mypage')
def mypage():
    try:
        return render_template('fav.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/coffee')
def detail():
    return render_template('coffeeDetail.html')


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_receive = request.form['nick_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    count = list(db.user.find({}, {'_id': False}))
    num = len(count) + 1

    db.user.insert_one({'uid':num, 'id': id_receive, 'pw': pw_hash, 'nick': nick_receive, 'fav':[]})

    return jsonify({'result': 'success'})

# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [아이디 중복 확인 API]
@app.route('/api/idCheck', methods=['GET'])
def api_id_check():
    id_receive = request.args.get('id')

    if db.user.find_one({"id": id_receive}) is None:
        return jsonify({'result': 'available'})
    else:
        return jsonify({'result': 'unavailable'})

# [닉네임 중복 확인 API]
@app.route('/api/nickCheck', methods=['GET'])
def api_nick_check():
    nick_receive = request.args.get('nick')

    if db.user.find_one({"nick": nick_receive}) is None:
        return jsonify({'result': 'available'})
    else:
        return jsonify({'result': 'unavailable'})



#################################
##  메인 페이지 음료 리스트 API  ##
#################################

@app.route("/slide", methods=['GET'])
def slide_GET():
    coffee_list = list(db.coffee.find({}, {'_id': False}))
    return jsonify({'lists':coffee_list})

@app.route("/ediya", methods=['GET'])
def ediya_GET():
    ediya_list = list(db.coffee.find({'cafe': 'ediya'}, {'_id': False}))
    return jsonify({'ediya':ediya_list})

@app.route("/starbucks", methods=['GET'])
def starbucks_GET():
    ediya_list = list(db.coffee.find({'cafe': 'starbucks'}, {'_id': False}))
    return jsonify({'starbucks':ediya_list})

@app.route("/hollys", methods=['GET'])
def hollys_GET():
    ediya_list = list(db.coffee.find({'cafe': 'hollys'}, {'_id': False}))
    return jsonify({'hollys':ediya_list})

@app.route("/paikdabang", methods=['GET'])
def dabang_GET():
    ediya_list = list(db.coffee.find({'cafe': "paikdabang"}, {'_id': False}))
    return jsonify({'paikdabang':ediya_list})

@app.route("/favorites_send", methods=['POST'])
def favorites_send():
    coffee_id = int(request.form['coffee_id']) # 커피이름을 눌렀을때 나오는 coffee_id

    current_favorites_number = db.coffee.find_one({'coffee_id': coffee_id})
    number = int(current_favorites_number['favorites'])
    favorites_number = number + 1
    db.coffee.update_one({'coffee_id': coffee_id},{'$set':{'favorites': favorites_number}})
    return jsonify({'msg': coffee_id})


#################################
##마이페이지 즐겨찾기 리스트 API ##
#################################

@app.route("/coffees", methods=["GET"])
def fave_get():


    fav_list = [10,15,30,50,90,100,200,300,250,240,105]
    # # for i in fav_list:
    # #     a=(db.coffee.find({'coffee_id' : i},{'_id':False}))
    # #     print("print a " + str(a))
    return_list = []
    for i in fav_list:
        for a in db.coffee.find({'coffee_id' : i},{'_id':False}):
            return_list.append(a)

    # print(return_list)

    return jsonify({'coffees':return_list})

@app.route("/delfav", methods=["post"])
def web_mars_add():
    id_receive = request.form['id_give']
    coffee_id_receive = request.form['coffee_name_give']
    return_list_receive = request.form['return_list_give']

    fav_list = db.users.delete_one(return_list_receive)
    return jsonify({'msg':'삭제완료' })


#################################
##        커피상세정보 API      ##
#################################

# 커피상세정보 GET
@app.route('/coffee/1', methods=["GET"])
def get_coffee_detail():
    coffee_detail = list(db.coffee.find({'coffee_id': 1}, {'_id': False}))
    # print(coffee_detail)
    return jsonify({'detail': coffee_detail})

#comment GET
@app.route('/comment', methods=["GET"])
def get_coffee_comment():
    coffee_comment = list(db.comment.find({}, {'_id': False}))
    # print(coffee_comment)
    return jsonify({'comment': coffee_comment})

#comment POST
@app.route("/comment", methods=["POST"])
def post_coffee_comment():
    comment_receive = request.form['comment_give']
    id_receive = request.form['id_give']

    # bucket_list = list(db.bucket.find({}, {'_id': False}))
    # count = len(bucket_list) + 1

    doc = {
        'id': id_receive,
        'comment': comment_receive
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
