import os
import sys
import traceback
import json
import networkx as nx

from flask import Flask, request, jsonify, abort

from rnamigos_launcher import launch
from networkx.readwrite import json_graph
import networkx as nx

import tempfile

app = Flask(__name__)


@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app.route("/rnamigos", methods=['POST'])
def rnamigos():
    result_rnamigos = {}

    G_list = []
    G = None
    if 'graph' in request.files:
        try:
            f = request.files['graph']
            data = json.load(f)
            for graph_id, graph_dict in data['graphs'].items():
                G = nx.Graph()
                G.add_edges_from(graph_dict['edges'])
                G.add_nodes_from(graph_dict['nodes'])
                G_list.append((graph_id, G))
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

    # print(result_rnamigos)
    return result_rnamigos


@app.route("/rnamigos_pipeline", methods=['POST'])
def rnamigos():
    '''
    Runs RNAMigos in the context of the pipeline.

    In addition to a ligand library, this receives graphs per motif for possibly
    multiple sequences.

    :returns: jsonified output of RNAMigos in terms of each motif per sequence
    '''
    if ("graphs" not in request.form):
        abort(400, "Did not receive any graphs to process.")
    if ("library" not in request.files):
        abort(400, "Did not receive a ligand library")

    result_rnamigos = {}
    processed_graphs = {}

    try:
        bp_output = eval(request.form.get("graphs"))
        processed_graphs = {}
        for sequence in bp_output.keys():
            graph_list = []
            motif_graph_mapping = bp_output.get(sequence)
            for module_id, graph_dict in motif_graph_mapping.items():
                graph = nx.Graph()
                graph.add_edges_from(graph_dict['edges'])
                graph.add_nodes_from(graph_dict['nodes'])
                graph_list.append((module_id, graph))
            processed_graphs[sequence] = graph_list
    except Exception as e:
        abort(400, "Could not process graph input: " + str(e))

    final_output = {}

    ligand_library = request.files['ligand_library']

    try:
        ligand_library.seek(0)
        temp = tempfile.NamedTemporaryFile()
        ligand_library.seek(0)
        temp.write(ligand_library.read())
        temp.seek(0)
        library_path = temp.name

    except Exception as e:
        abort(400, "Could not process ligand library: " + str(e))

    try:
        for sequence in processed_graphs.keys():
            graph_list = processed_graphs.get(sequence)
            for module_id, graph in graph_list:
                result_rnamigos[module_id] = launch(graph, library_path)
            final_output[sequence] = result_rnamigos
    except Exception as e:
        abort(400, "RNAMigos failed to complete: " + str(e))

    temp.close()
    return jsonify(final_output)


@app.route('/', methods=['GET'])
def hello():
    return jsonify(about='Hello from RNAmigos, WP!')


# it appears that it is unnecessary to specify the port/localhost
if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)
