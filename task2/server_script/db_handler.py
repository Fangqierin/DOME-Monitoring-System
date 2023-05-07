import json
import os
import sys
import math
import requests
import ast

import numpy as np
from flask import Flask, send_file, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import json_util
from config import *

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/dome'  # Replace with your MongoDB URI
mongo = PyMongo(app)


@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        collection_name = request.args.get('collection_name')
        limit_num = request.args.get('limit_num')
        collection = mongo.db[collection_name]
        data = collection.find().sort([('_id', -1)]).limit(int(limit_num) if limit_num else 0)
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
        data = collection.find().sort([('filename', -1)])
        return json_util.dumps({'result': data})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/waypoint', methods=['GET'])
def get_waypoints():
    try:
        not_drone = request.args.get('not_drone')
        manual = request.args.get('manual')

        collection_task_config = mongo.db['task_config']
        task_config = collection_task_config.find_one({})

        collection_grid = mongo.db['grids']

        if not not_drone and (task_config['trigger'] or manual):
            fire_data = list(collection_grid.find())

            # Use fire status data to update waypoints
            size = (4, 3)  # Fire Setting Grid Size
            grids = np.full((size[0], size[1]), 0)

            for f in fire_data:
                for fire in json.loads(f['data'])['fires']:
                    col, row = min(math.floor((fire['fx']) / 50), 2), min(math.floor((-fire['fy'] + 200) / 50), 3)
                    col, row = max(col,  0), max(row, 0)
                    grids[row][col] = 1


            missions = task_config['param']
            plan = task_config['env']['plan_time']
            wind = task_config['env']['wind_speed']
            direction = task_config['env']['direction']
            data = {
                'Missions': missions,
                'Grid_map': grids.tolist(),
                'Plan': plan,
                'Wind':wind,
                'Direction': direction
            }

            # Send POST request
            url = 'http://192.168.82.131:5000/process_data'
            response = requests.post(url, json=data)
            # Check response status code
            if response.status_code == 200:
                answer=json.loads(response.text)
                estimated_fire_arrival_time = answer['EFA']
                waypoints=answer['WPS']
                tasks=answer['Task']
                
                collection_waypoints = mongo.db['waypoints']
                collection_waypoints.delete_many({})
                for waypoint in waypoints:
                    collection_waypoints.insert_one({
                        "x": waypoint[0] * 50,
                        "y": waypoint[1] * 50,
                        "z": waypoint[2] * 50
                    })
                
                reformatted_tasks = []
                for key, value in tasks.items():
                    value = ast.literal_eval(value)
                    x, y = ast.literal_eval(key)
                    reformatted_tasks.append(
                        {"x": y, "y": 2 - x, "task": value}
                    )

                collection_processed_data = mongo.db['processed_data']
                collection_processed_data.delete_many({})
                collection_processed_data.insert_one({
                    "grids": grids.tolist(),
                    "estimated_fire_arrival_time": estimated_fire_arrival_time,
                    "tasks": reformatted_tasks
                })
                
                
            else:
                print('POST request failed with status code', response.status_code)

            # TODO: this line should be replaced by a post request when the remote server is on
            '''
            tasks, estimated_fire_arrival_time, waypoints = (
                {
                    (3, 2): {'FI': (0, -1)},
                    (3, 1): {'FI': (0, -1)},
                    (3, 0): {'FI': (0, -1)},
                    (2, 2): {'FI': (0, -1)},
                    (2, 1): {'FI': (0, -1)},
                    (2, 0): {'FI': (0, -1)},
                    (1, 2): {'FI': (0, -1)},
                    (1, 1): {'FI': (0, -1)},
                    (1, 0): {'FI': (0, -1)},
                    (0, 2): {'FI': (0, -1)},
                    (0, 1): {'FI': (0, -1)},
                    (0, 0): {'FI': (0, -1)}
                },
                [[100] * 3 for i in range(4)],
                [[125, 175, 100], [25, 25, 100], [25, 175, 100], [75, 175, 100], [125, 175, 100], [125, 125, 100],
                 [75, 125, 100], [25, 125, 100], [25, 75, 100], [75, 75, 100], [125, 75, 100], [125, 25, 100],
                 [75, 25, 100], [25, 25, 100]]
            )
            '''
            collection_grid.delete_many({})

        collection = mongo.db['waypoints']
        documents = list(collection.find())

        return json_util.dumps(documents)

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


@app.route('/processed_data', methods=['GET'])
def get_processed_data():
    try:
        collection = mongo.db['processed_data']
        data = collection.find_one({})

        return json_util.dumps({'result': data})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/task_config', methods=['GET'])
def get_task_config():
    try:
        collection = mongo.db['task_config']
        data = collection.find_one({})

        return json_util.dumps({'result': data})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/task_config', methods=['POST'])
def overwrite_task_config():
    try:
        collection = mongo.db['task_config']
        data = request.get_json()
        collection.replace_one({}, data)
        return jsonify({'message': 'Task config updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


# reset images data for dev use only
@app.route('/replace_data', methods=['GET'])
def replace_data():
    try:
        collection = mongo.db['images']
        collection.delete_many({})

        newdata = [{"_id": {"$oid": "6403c4484856f667d7a2f7f8"}, "filename": "preview3.jpg",
                    "filepath": "images\\preview3.jpg"},
                   {"_id": {"$oid": "6403c4484856f667d7a2f7f7"}, "filename": "preview2.jpg",
                    "filepath": "images\\preview2.jpg"},
                   {"_id": {"$oid": "6403c4484856f667d7a2f7f6"}, "filename": "preview1.jpg",
                    "filepath": "images\\preview1.jpg"},
                   {"_id": {"$oid": "6403c3a604e5195e39ce7a55"}, "filename": "logo192.jpg",
                    "filepath": "images\\logo192.jpg"}]

        for data in newdata:
            data.pop('_id')
            collection.insert_one(data)

        return jsonify({'message': 'Updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


def init():
    # empty the images collection
    try:
        collection = mongo.db['images']
        collection.delete_many({})
    except Exception as e:
        print(e)

    # initialize the task config
    try:
        collection = mongo.db['task_config']
        data = collection.find_one({})
        if not data:
            data = {
                "param": {
                    "BM": [
                        1,
                        1
                    ],
                    "FI": [
                        0.5,
                        1
                    ],
                    "FT": [
                        1,
                        1
                    ],
                    "FD": [
                        0.5,
                        1
                    ]
                },
                "env": {
                    "wind_speed": 5,
                    "plan_time": 1,
                    "direction": 271
                },
                "trigger": True
            }
            collection.insert_one(data)
    except Exception as e:
        print(e)

    # initialize the processed data:
    try:
        collection = mongo.db['processed_data']
        data = collection.delete_one({})
        tasks, estimated_fire_arrival_time = (
            {
                (3, 2): {'FI': (0, -1)},
                (3, 1): {'FI': (0, -1)},
                (3, 0): {'FI': (0, -1)},
                (2, 2): {'FI': (0, -1)},
                (2, 1): {'FI': (0, -1)},
                (2, 0): {'FI': (0, -1)},
                (1, 2): {'FI': (0, -1)},
                (1, 1): {'FI': (0, -1)},
                (1, 0): {'FI': (0, -1)},
                (0, 2): {'FI': (0, -1)},
                (0, 1): {'FI': (0, -1)},
                (0, 0): {'FI': (0, -1)}
            },
            [[100] * 3 for i in range(4)]
        )

        reformatted_tasks = []
        for key, value in tasks.items():
            x, y = key
            reformatted_tasks.append(
                {"x": x, "y": y, "task": value}
            )

        collection_processed_data = mongo.db['processed_data']
        collection_processed_data.delete_many({})
        collection_processed_data.insert_one({
            "grids": [[0] * 3 for i in range(4)],
            "estimated_fire_arrival_time": estimated_fire_arrival_time,
            "tasks": reformatted_tasks
        })
        data = collection.find_one({})
    except Exception as e:
        print(e)

    # initialize waypoints
    collection = mongo.db['waypoints']
    documents = list(collection.find())

    if not documents:
        default_waypoints = [
            {"_id": {"$oid": "644b4924cbdb2c1461b20073"}, "x": 125, "y": 175, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b20072"}, "x": 25, "y": 25, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b20071"}, "x": 25, "y": 175, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b20070"}, "x": 75, "y": 175, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b2006f"}, "x": 125, "y": 175, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b2006e"}, "x": 125, "y": 125, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b2006d"}, "x": 75, "y": 125, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b2006c"}, "x": 25, "y": 125, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b2006b"}, "x": 25, "y": 75, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b2006a"}, "x": 75, "y": 75, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b20069"}, "x": 125, "y": 75, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b20068"}, "x": 125, "y": 25, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b20067"}, "x": 75, "y": 25, "z": 100},
            {"_id": {"$oid": "644b4924cbdb2c1461b20066"}, "x": 25, "y": 25, "z": 100}]
        for waypoint in default_waypoints:
            waypoint.pop('_id')
            collection.insert_one(waypoint)
            
    
    # empty sensor data
    collection = mongo.db['air']
    collection.delete_many({})
    
        
    collection = mongo.db['weather']
    collection.delete_many({})


if __name__ == '__main__':
    init()
    app.run(debug=True, host='0.0.0.0', port=5555)
