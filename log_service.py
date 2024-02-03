from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import jwt


app = Flask(__name__)
app.config['SECRET_KEY'] = '8606305727anamikaapp'
client = MongoClient("mongodb://localhost:27017/")
app.debug = True

db = client["Users"]

@app.route('/log/register', methods=['POST'])
def log_register():
    
    # loging user data data every time user added and saving that details in db
    data = request.json
    response = db["activity_logs"].insert_one({'activity': 'register', 'data': data})
    if not response.acknowledged:
        return jsonify(message = "log activity Insertion Failed"),400
    return jsonify(message='Registration activity logged successfully'),200

@app.route('/log/login', methods=['POST'])
def log_login():
    
    data = request.json
    # Log login activity and store in db
    response = db["activity_logs"].insert_one({'activity': 'login', 'data': data})
    if not response.acknowledged:
        return jsonify(message = "log activity Insertion Failed"),400
    return jsonify(message='Login activity logged successfully'),200

@app.route('/log/api-key', methods=['POST'])
def log_api_key():
    
    data = request.json
    # Logging api key
    response = db["activity_logs"].insert_one({'activity': 'api_key_generation', 'data': data})
    if not response.acknowledged:
        return jsonify(message = "log activity Insertion Failed"),400
    return jsonify(message='API key generation activity logged successfully'),200

@app.route('/logs', methods=['GET'])
def get_logs():
    token = request.headers.get('Authorization')
    try:
        
        # Fetching logs only for Authorized users
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        logs = list(db["activity_logs"].find({}, {'_id': 0}))
        
        if not logs:
            return jsonify(logs = "No Logs listed for this user"),200
        return jsonify(logs=logs),200
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token has expired'), 401
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token'), 401

if __name__ == '__main__':
    app.run(debug=True)