from flask import Flask, request, jsonify
from pymongo import MongoClient
import jwt
import random
import bcrypt
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '8606305727anamikaapp'
client = MongoClient("mongodb://localhost:27017/")
app.debug = True

@app.route('/generate-api-key', methods=['POST'])
def generate_api_key():
    token = request.headers.get('Authorization')
    try:
        # checking for that user existence and authorization
        jwt.decode(token,app.config['SECRET_KEY'], algorithms=['HS256'])
        username = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['username']
        
        # Generate a random API key
        api_key = str(random.randint(100000, 999999))
        db = client["Users"]
        
        # Associate API key with the authenticated user
        response = db["api_keys"].insert_one({'username': username, 'api_key': api_key})
        if not response.acknowledged:
            return jsonify(msg='Failed to insert api keys'),400
        return jsonify(api_key=api_key)
    except jwt.ExpiredSignatureError:
        return jsonify(msg='Token has expired'), 400
    except jwt.InvalidTokenError:
        return jsonify(msg='Invalid token'), 400
    

if __name__ == '__main__':
    app.run(debug=True)