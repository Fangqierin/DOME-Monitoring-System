from flask import Flask, send_file, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import json_util
from config import *

import os

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/dome'  # Replace with your MongoDB URI
mongo = PyMongo(app)


@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        collection_name = request.args.get('collection_name')
        collection = mongo.db[collection_name]
        data = collection.find().sort([('_id', -1)]).limit(9 if collection_name == "images" else 5)
        return json_util.dumps({'result': list(data)})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_image/<path:filename>')
def get_image(filename):
    try:
        filepath = os.path.join(IMAGE_DIR, filename)
        return send_file(filepath, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_grids')
def get_grids():
    try:
        collection = mongo.db['grids']
        data = collection.find().sort([('_id', -1)])
        return json_util.dumps({'result': data})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/waypoint', methods=['GET'])
def get_unread_waypoints():
    try:
        collection = mongo.db['way_points']
        documents = list(collection.find({"read": "0"}))
        for doc in documents:
            collection.update_one({'_id': doc['_id']}, {'$set': {'read': '1'}})
            doc['read'] = '1'
        return jsonify(documents)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/waypoint', methods=['POST'])
def add_waypoint():
    try:
        collection = mongo.db['way_points']
        data = request.json
        collection.insert_one({
            'x': data['x'],
            'y': data['y'],
            'z': data['z'],
            'read': data['read']
        })
        return jsonify({'message': 'Waypoint added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
