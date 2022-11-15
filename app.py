from flask import Flask, render_template, request, jsonify
import random
from random import *
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.ffudy0q.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.coffeeduckhu

@app.route('/')
def index():
    result = []
    for i in range(8):
        j = randint(1, 342)
        test = db.coffee.find_one({'coffee_id': j})
        url = test['coffee_image']
        result.append(url)

    return render_template('index.html', variable=result)

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
    coffee_id = request.form['coffee_id']
    return jsonify({'msg': coffee_id})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)