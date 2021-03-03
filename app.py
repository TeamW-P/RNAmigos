import os
import sys
import traceback
import json
import networkx as nx

from flask import Flask, request, jsonify

from rnamigos_launcher import launch
from networkx.readwrite import json_graph
import networkx as nx

import tempfile

app = Flask(__name__)

@app.route("/rnamigos", methods=['POST'])
def rnamigos():
    result_rnamigos = {}
    
    G_list = []
    G = None
    res = {}
    if 'graph' in request.files:
        try:
            f = request.files['graph']
            data = json.load(f)
            for graph_id, graph_dict in data['graphs'].items():
                G = nx.Graph()
                G.add_edges_from(graph_dict['edges'])
                G.add_nodes_from(graph_dict['nodes'])
                G_list.append((graph_id,G))
        except Exception as e:
            print("Failed to upload the graph file")
            print(e)
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

    try:
        for graph_id, G in G_list:
            result_json = launch(G, library)
            result_rnamigos[graph_id] = result_json

    except:
        print(traceback.format_exc())

    return jsonify(result_rnamigos)

@app.route('/', methods=['GET'])
def hello():
    return jsonify(about='Hello from RNAmigos, WP!')

# it appears that it is unnecessary to specify the port/localhost
if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)