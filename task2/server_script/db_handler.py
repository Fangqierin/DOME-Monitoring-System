import os
import sys

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
def get_waypoints():
    try:
        collection_grid = mongo.db['grids']
        fire_data = list(collection_grid.find())

        if fire_data:
            # Use fire status data to update waypoints
            size = (3, 4)  # Fire Setting Grid Size
            grids = np.full((size[0], size[1]), 0)
            grids[0, 0] = 0
            grids[1, 0] = 0
            grids[2, 1] = 1

            tasks, estimated_fire_arrival_time, waypoints = (
                {
                    (3, 4): {'BM': (0, 3), 'FT': (0, -1)},
                    (3, 3): {'FT': (0, -1)},
                    (3, 2): {'FT': (0, -1)},
                    (3, 1): {'FT': (0, -1)},
                    (3, 0): {'FT': (0, -1)},
                    (2, 4): {'BM': (0, 3), 'FT': (0, -1)},
                    (2, 3): {'BM': (0, 3), 'FT': (0, -1)},
                    (2, 2): {'FI': (0, -1)},
                    (2, 1): {'FI': (0, -1)},
                    (2, 0): {'FI': (0, -1)},
                    (1, 4): {'BM': (0, 3), 'FT': (0, -1)},
                    (1, 3): {'BM': (0, 3), 'FT': (0, -1)},
                    (1, 2): {'FI': (0, -1)},
                    (1, 1): {'FI': (0, -1)},
                    (1, 0): {'FI': (0, -1)},
                    (0, 4): {'BM': (0, 6), 'FT': (0, -1)},
                    (0, 3): {'BM': (0, 3), 'FT': (0, -1)},
                    (0, 2): {'FI': (0, -1)},
                    (0, 1): {'FI': (0, -1)},
                    (0, 0): {'FI': (0, -1)}
                },
                [[0, 0, 0, 6, 9],
                 [0, 0, 0, 6, 6],
                 [0, 0, 0, 6, 6],
                 [3, 3, 3, 3, 6]],
                [(0.5, 0.5, 0), (0.5, 0.5, 1.1), (1.5, 0.5, 1.1), (2.5, 0.5, 1.1), (2.5, 1.5, 1.1), (1.5, 1.5, 1.1),
                 (0.5, 1.5, 1.1), (0.5, 2.5, 1.1), (1.5, 2.5, 1.1), (2.5, 2.5, 1.1), (2.5, 3.5, 1.1), (1.5, 3.5, 1.1),
                 (1.5, 4.5, 1.1), (2.5, 4.5, 1.1), (3.5, 4.5, 1.1), (0.5, 4.5, 1.1), (0.5, 3.5, 1.1), (3.5, 3.5, 1.1),
                 (3.5, 2.5, 1.1), (3.5, 1.5, 1.1), (3.5, 0.5, 1.1), (2.5, 0.5, 1.1), (1.5, 0.5, 1.1), (0.5, 0.5, 1.1),
                 (0.5, 1.5, 1.1), (1.5, 1.5, 1.1), (2.5, 1.5, 1.1), (2.5, 2.5, 1.1), (1.5, 2.5, 1.1), (0.5, 2.5, 1.1),
                 (1.5, 2.5, 1.1), (2.5, 2.5, 1.1), (2.5, 1.5, 1.1), (1.5, 1.5, 1.1), (0.5, 1.5, 1.1), (0.5, 0.5, 1.1),
                 (1.5, 0.5, 1.1), (2.5, 0.5, 1.1), (2.5, 3.5, 1.1), (1.5, 3.5, 1.1), (1.5, 4.5, 1.1), (2.5, 4.5, 1.1),
                 (3.5, 4.5, 1.1), (0.5, 4.5, 1.1), (0.5, 3.5, 1.1), (3.5, 3.5, 1.1), (3.5, 2.5, 1.1), (3.5, 1.5, 1.1),
                 (3.5, 0.5, 1.1), (2.5, 0.5, 1.1), (1.5, 0.5, 1.1), (0.5, 0.5, 1.1), (0.5, 1.5, 1.1), (1.5, 1.5, 1.1),
                 (2.5, 1.5, 1.1), (2.5, 2.5, 1.1), (1.5, 2.5, 1.1), (0.5, 2.5, 1.1), (1.5, 2.5, 1.1), (2.5, 2.5, 1.1),
                 (2.5, 1.5, 1.1), (1.5, 1.5, 1.1), (0.5, 1.5, 1.1), (0.5, 0.5, 1.1), (1.5, 0.5, 1.1), (2.5, 0.5, 1.1),
                 (2.5, 3.5, 1.1), (1.5, 3.5, 1.1), (1.5, 4.5, 1.1), (2.5, 4.5, 1.1), (3.5, 4.5, 1.1), (0.5, 4.5, 1.1),
                 (0.5, 3.5, 1.1), (3.5, 3.5, 1.1), (3.5, 2.5, 1.1), (3.5, 1.5, 1.1), (3.5, 0.5, 1.1), (2.5, 0.5, 1.1),
                 (1.5, 0.5, 1.1), (0.5, 0.5, 1.1), (0.5, 1.5, 1.1), (1.5, 1.5, 1.1), (2.5, 1.5, 1.1), (2.5, 2.5, 1.1),
                 (1.5, 2.5, 1.1), (0.5, 2.5, 1.1), (1.5, 2.5, 1.1), (2.5, 2.5, 1.1), (2.5, 1.5, 1.1), (1.5, 1.5, 1.1),
                 (0.5, 1.5, 1.1), (0.5, 0.5, 1.1), (1.5, 0.5, 1.1), (2.5, 0.5, 1.1), (0.5, 4.5, 1.1), (1.5, 4.5, 1.1),
                 (1.5, 3.5, 1.1), (2.5, 3.5, 1.1), (2.5, 4.5, 1.1), (3.5, 4.5, 1.1), (0.5, 3.5, 1.1), (3.5, 3.5, 1.1),
                 (3.5, 2.5, 1.1), (3.5, 1.5, 1.1), (3.5, 0.5, 1.1), (2.5, 0.5, 1.1), (1.5, 0.5, 1.1), (0.5, 0.5, 1.1),
                 (0.5, 1.5, 1.1), (1.5, 1.5, 1.1), (2.5, 1.5, 1.1), (2.5, 2.5, 1.1), (1.5, 2.5, 1.1), (0.5, 2.5, 1.1)]
            )

            collection_waypoints = mongo.db['waypoints']
            collection_waypoints.delete_many({})
            for waypoint in waypoints:
                collection_waypoints.insert_one({
                    "x": waypoint[0],
                    "y": waypoint[1],
                    "z": waypoint[2]
                })

            reformatted_tasks = []
            for key, value in tasks.items():
                x, y = key
                reformatted_tasks.append(
                    {"x": x, "y": y, "task": value}
                )

            collection_processed_data = mongo.db['processed_data']
            collection_processed_data.delete_many({})
            collection_processed_data.insert_one({
                "grids": grids.tolist(),
                "estimated_fire_arrival_time": estimated_fire_arrival_time,
                "tasks": reformatted_tasks
            })

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
