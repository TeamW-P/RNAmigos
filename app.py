from flask import Flask, jsonify
#from routes import *

app = Flask(__name__)
#app.register_blueprint(routes)

@app.route('/', methods=['GET'])
def hello():
    return jsonify(about='Hello from RNAmigos, WP!')

# it appears that it is unnecessary to specify the port/localhost
if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)