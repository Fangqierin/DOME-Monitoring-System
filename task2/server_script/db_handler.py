from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/dome'  # Replace with your MongoDB URI
mongo = PyMongo(app)


@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        collection_name = request.args.get('collection_name')
        collection = mongo.db[collection_name]
        data = collection.find().sort([('_id', -1)]).limit(5)
        output = []
        for d in data:
            output.append({'data': d['data']})  # Replace 'data' with the name of the field you want to retrieve
        return jsonify({'result': output})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
