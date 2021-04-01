import os
import sys
import traceback
import json
import networkx as nx
import errno

from flask import Flask, request, jsonify, abort, Blueprint

from core.src import rnamigos_launcher
from networkx.readwrite import json_graph
import networkx as nx

import tempfile


app = Flask(__name__)
routes = Blueprint("routes", __name__)

@routes.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@routes.route("/rnamigos-string", methods=['POST'])
def rnamigos_string():
    '''
    Runs RNAMigos in the context of the pipeline for testing purposes.

    Receives graphs per motif for possibly multiple sequences in string format, and an optional ligand library.

    :returns: jsonified output of RNAMigos in terms of each motif per sequence.
    '''

    if ("graphs" not in request.form):
        abort(400, "Did not receive any graphs to process.")

    result_rnamigos = {}
    processed_graphs = {}

    try:
        bp_output = eval(request.form.get("graphs"))
        processed_graphs = {}
        for sequence in bp_output.keys():
            graph_list = []
            motif_graph_mapping = bp_output[sequence]
            for module_id, graph_dict in motif_graph_mapping.items():
                graph = nx.Graph()
                graph.add_edges_from(graph_dict['edges'])
                graph.add_nodes_from(graph_dict['nodes'])
                graph_list.append((module_id, graph))
            processed_graphs[sequence] = graph_list
    except Exception as e:
        abort(400, "Could not process graph input: " + str(e))

    final_output = {}

    library_path = None

    temp = tempfile.NamedTemporaryFile()

    if 'library' in request.files:
        try:
            ligand_library = request.files['library']
            ligand_library.seek(0)
            temp.write(ligand_library.read())
            temp.seek(0)
            library_path = temp.name
            final_output['rnamigos_library'] = ligand_library.filename
            if ligand_library.filename.split('.')[-1] != "txt":
                raise ValueError("Rnamigos library needs to be in .txt format")
            if os.stat(library_path).st_size == 0:
                raise ValueError("Rnamigos library can't be empty")

        except Exception as e:
            abort(400, "Could not process ligand library: " + str(e))

    try:
        for sequence in processed_graphs.keys():
            graph_list = processed_graphs[sequence]
            for module_id, graph in graph_list:
                result_rnamigos[module_id] = rnamigos_launcher.launch(graph, library_path)
            final_output[sequence] = result_rnamigos
    except Exception as e:
        abort(400, "RNAMigos failed to complete: " + str(e))

    temp.close()
    return jsonify(final_output)
