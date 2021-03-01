import os
import sys
import traceback
import json

from flask import Flask, request, jsonify

from rnamigos_launcher import launch
from networkx.readwrite import json_graph

import tempfile

app = Flask(__name__)

@app.route("/rnamigos", methods=['POST'])
def rnamigos():
    G = None
    if 'graph' in request.files:
        try:
            f = request.files['graph']
            temp = tempfile.NamedTemporaryFile()
            tempname = temp.name
            f.seek(0)
            temp.write(f.read())
            temp.seek(0)
            data = json.load(temp)
            print(data)
            G = json_graph.node_link_data(data)
            print(G)

        except Exception as e:
            print("Failed to upload the graph file")
            pass

    library = None
    if 'library' in request.files:
        try:
            f = request.files['library']
            temp = tempfile.NamedTemporaryFile()
            tempname = temp.name
            f.seek(0)
            temp.write(f.read())
            temp.seek(0)
            library = tempname

        except Exception as e:
            print("Failed to upload the library file")
            pass

    """
    try:
        result_json = launch(G, library)
        return result_json

    except:
        print(traceback.format_exc())
    """

    result_json = launch(G, library)
    return result_json

@app.route('/', methods=['GET'])
def hello():
    return jsonify(about='Hello from RNAmigos, WP!')

# it appears that it is unnecessary to specify the port/localhost
if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)