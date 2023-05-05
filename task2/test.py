from flask import Flask
import random

app = Flask(__name__)

@app.route('/test')
def test():
    num = str(random.randint(1, 100))
    print(num)
    return num

if __name__ == '__main__':
    # Listen on all available network interfaces on port 3000
    app.run(debug=True, host='0.0.0.0', port=3000)