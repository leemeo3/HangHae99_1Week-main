from flask import Flask, render_template, request, jsonify, redirect, url_for
from random import *

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.ffudy0q.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.coffeeduckhu

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
    favorite = []
    best_list = list(db.coffee.find({}, {'coffee_id': 1, 'favorites': 1, 'coffee_image': 1}).sort('favorites', -1).limit(8))
    for best in best_list:
        url = best['coffee_image']
        fav = best['favorites']
        # j = randint(1, 342)
        # test = db.coffee.find_one({'coffee_id': j})
        # url = test['coffee_image']
        result.append(url)
        favorite.append(fav)

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', variable=result, favorites=favorite, nickname=user_info["nick"], uid=user_info["uid"])
    except jwt.ExpiredSignatureError:

        return render_template('index.html', variable=result, favorites=favorite)
    except jwt.exceptions.DecodeError:
        return render_template('index.html', variable=result, favorites=favorite)

@app.route('/login')
def login():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('fav.html', nickname=user_info["nick"], uid=user_info["uid"])
    except jwt.ExpiredSignatureError:
        return render_template('login.html')
    except jwt.exceptions.DecodeError:
        return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/mypage/<uid>')
def mypage(uid):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        if user_info['uid'] == int(uid):
            return render_template('fav.html', nickname=user_info["nick"], uid=user_info["uid"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/coffee/<coffee_id>')
def detail(coffee_id):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('coffeeDetail.html', coffee_id=coffee_id, nickname=user_info["nick"], uid=user_info["uid"])
    except jwt.ExpiredSignatureError:
        return render_template('coffeeDetail.html', coffee_id=coffee_id)
    except jwt.exceptions.DecodeError:
        return render_template('coffeeDetail.html', coffee_id=coffee_id)


##############################
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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [아이디 중복 확인 API]
@app.route('/api/idCheck', methods=['POST'])
def api_id_check():
    id_receive = request.form['id_give']

    if db.user.find_one({"id": id_receive}) is None:
        return jsonify({'result': 'available'})
    else:
        return jsonify({'result': 'unavailable'})

# [닉네임 중복 확인 API]
@app.route('/api/nickCheck', methods=['POST'])
def api_nick_check():
    nick_receive = request.form['nick_give']

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
    coffee_id = int(request.form['coffee_id'])
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})

        # 즐겨찾기 카운트 증가
        current_favorites_number = db.coffee.find_one({'coffee_id': coffee_id})
        number = int(current_favorites_number['favorites'])
        favorites_number = number + 1

        uid = int(user_info["uid"]) # uid 저장 int 10
        detail = db.user.find_one({'uid': uid, 'fav.coffee_id': coffee_id}, {'_id': False})

        if detail is None:
            db.coffee.update_one({'coffee_id': coffee_id}, {'$set': {'favorites': favorites_number}})
            db.user.update_one({'uid': uid}, {'$push': {'fav': {'coffee_id': coffee_id}}})
            return jsonify({'msg': '즐겨찾기 등록이 완료되었습니다.', 'cafe': coffee_id})
        else:
            return jsonify({'msg': '이미 즐겨찾기 목록에 들어 있습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'msg': '로그인을 해주세요.'})
    except jwt.ExpiredSignatureError:
        return jsonify({'msg': '로그인을 해주세요.'})


#################################
##마이페이지 즐겨찾기 리스트 API ##
#################################
# db.user.update_one({'uid': fave_id}, {'$set': {'fav': [{'coffee_id':1}, {'coffee_id':2}, {'coffee_id':20}, {'coffee_id':30}, {'coffee_id':60}, {'coffee_id':100}, {'coffee_id':200}, {'coffee_id':300}, {'coffee_id':231}]}})
@app.route("/api/mypage/<fave_id>", methods=["GET"])
def mypage_detail(fave_id):
    fave_id = int(fave_id)
    # 유저 id와 받아온 id가 같은 데이터
    mypage_detail = db.user.find_one({"uid": fave_id}, {'_id': False})
    # 데이터중 fav 데이터만 출력
    fav_all= list(mypage_detail['fav'])
    fav_num=[]
    # fav데이터 추출한부분의 총길이만큼 반복
    for coffee_id in fav_all:
        fav_num.append(coffee_id['coffee_id'])
    all_menu=[]
    for i in fav_num:
        for x in db.coffee.find({'coffee_id':i},{'_id':False}):
            all_menu.append(x)
    return jsonify({'mypage_detail': all_menu})


#즐겨찾기 스타벅스 메뉴 출력
@app.route("/star_menu/<fave_id>" , methods=['GET'])
def star_menu(fave_id):
    fave_id = int(fave_id)
    # 유저 id와 받아온 id가 같은 데이터
    mypage_detail = db.user.find_one({"uid": fave_id}, {'_id': False})
    # 데이터중 fav 데이터만 출력
    fav_all = list(mypage_detail['fav'])
    fav_num = []
    # fav데이터 추출한부분의 총길이만큼 반복
    for coffee_id in fav_all:
        fav_num.append(coffee_id['coffee_id'])
    all_menu = []
    for i in fav_num:
        for x in db.coffee.find({'coffee_id': i}, {'_id': False}):
            all_menu.append(x)
    return jsonify({'star': all_menu})

#즐겨찾기 할리스 메뉴 출력
@app.route("/hollys_menu/<fave_id>" , methods=['GET'])
def hollys_menu(fave_id):
    fave_id = int(fave_id)
    # 유저 id와 받아온 id가 같은 데이터
    mypage_detail = db.user.find_one({"uid": fave_id}, {'_id': False})
    # 데이터중 fav 데이터만 출력
    fav_all = list(mypage_detail['fav'])
    fav_num = []
    # fav데이터 추출한부분의 총길이만큼 반복
    for coffee_id in fav_all:
        fav_num.append(coffee_id['coffee_id'])
    all_menu = []
    for i in fav_num:
        for x in db.coffee.find({'coffee_id': i}, {'_id': False}):
            all_menu.append(x)
    return jsonify({'hollys': all_menu})

#즐겨찾기 이디야 메뉴 출력
@app.route("/ediya_menu/<fave_id>" , methods=['GET'])
def ediya_menu(fave_id):
    fave_id = int(fave_id)
    # 유저 id와 받아온 id가 같은 데이터
    mypage_detail = db.user.find_one({"uid": fave_id}, {'_id': False})
    # 데이터중 fav 데이터만 출력
    fav_all = list(mypage_detail['fav'])
    fav_num = []
    # fav데이터 추출한부분의 총길이만큼 반복
    for coffee_id in fav_all:
        fav_num.append(coffee_id['coffee_id'])
    all_menu = []
    for i in fav_num:
        for x in db.coffee.find({'coffee_id': i}, {'_id': False}):
            all_menu.append(x)
    return jsonify({'ediya': all_menu})
#즐겨찾기 빽다방 메뉴 출력
@app.route("/paik_menu/<fave_id>" , methods=['GET'])
def paik_menu(fave_id):
    fave_id = int(fave_id)
    # 유저 id와 받아온 id가 같은 데이터
    mypage_detail = db.user.find_one({"uid": fave_id}, {'_id': False})
    # 데이터중 fav 데이터만 출력
    fav_all = list(mypage_detail['fav'])
    fav_num = []
    # fav데이터 추출한부분의 총길이만큼 반복
    for coffee_id in fav_all:
        fav_num.append(coffee_id['coffee_id'])
    all_menu = []
    for i in fav_num:
        for x in db.coffee.find({'coffee_id': i}, {'_id': False}):
            all_menu.append(x)

    return jsonify({'paik': all_menu})

#즐겨찾기 전체 삭제
@app.route("/delfav", methods=["post"])
def del_all():
    uid_receive=int(request.form['uid_give'])
    db.user.update_one({'uid':uid_receive},{'$set': {'fav' : []}})
    return jsonify({'msg':'삭제완료'})

#즐겨찾기 한개 삭제
@app.route("/delfav_one", methods=["post"])
def del_one():
    uid_receive=int(request.form['uid_give'])
    btn_receive = int(request.form['coffe_id_give'])
    db.user.update_one({'uid':uid_receive},{'$pull': {'fav' : {'coffee_id':btn_receive}}})
    return jsonify({'msg':'삭제완료'})





#################################
##        커피상세정보 API      ##
#################################

# 커피상세정보 GET
@app.route('/api/coffee/<coffee_id>', methods=["GET"])
def get_coffee_detail(coffee_id):
    coffee_id = int(coffee_id)
    coffee_detail = list(db.coffee.find({'coffee_id': coffee_id}, {'_id': False}))
    # print(coffee_detail)
    return jsonify({'detail': coffee_detail})

#comment GET
@app.route('/api/comment/<coffee_id>', methods=["GET"])
def get_coffee_comment(coffee_id):
    coffee_id = int(coffee_id)
    coffee_comment = list(db.comment.find({'coffee_id': coffee_id}, {'_id': False}))
    return jsonify({'comment': coffee_comment})

#comment POST
@app.route("/api/comment/<coffee_id>", methods=["POST"])
def post_coffee_comment(coffee_id):
    coffee_id_receive = int(coffee_id)
    comment_receive = request.form['comment_give']
    id_receive = request.form['id_give']
    nickname_receive = request.form['nickname_give']


    doc = {
        'coffee_id': coffee_id_receive,
        'user_id': id_receive,
        'nickname': nickname_receive,
        'comment': comment_receive
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
