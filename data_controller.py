from flask import Flask, request, jsonify
from pymongo import MongoClient
import jwt
import random
import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '8606305727anamikaapp'
client = MongoClient("mongodb://localhost:27017/")
app.debug = True


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # encoding password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {'username': username, 
            'password': hashed_password}
    db = client["Users"]
    # saving to db
    response = db["users_data"].insert_one(user)
    if not response.acknowledged:
        return jsonify(msg='User Auth insertion Failed'), 400
    return jsonify(msg='User registered successfully'), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    db = client["Users"]
    # finding if that user exists
    user = db["users_data"].find_one({'username': username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # genrating jwt token for that user
        token = jwt.encode({'username': username},app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify(token=token)

    return jsonify(msg='Invalid credentials'), 401

if __name__ == '__main__':
    app.run(debug=True)