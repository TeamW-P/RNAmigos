"""
    Do inference on networkx graph to get fingerint.
"""
import pickle

import networkx as nx
import torch
import dgl

from rgcn import Model

nuc_map = {n:i for i,n in enumerate(['A', 'C', 'G', 'N', 'U'])}

def send_graph_to_device(g, device):
    """
    Send dgl graph to device
    :param g: :param device:
    :return:
    """
    g.set_n_initializer(dgl.init.zero_initializer)
    g.set_e_initializer(dgl.init.zero_initializer)

    # nodes
    labels = g.node_attr_schemes()
    for l in labels.keys():
        g.ndata[l] = g.ndata.pop(l).to(device, non_blocking=True)

    # edges
    labels = g.edge_attr_schemes()
    for i, l in enumerate(labels.keys()):
        g.edata[l] = g.edata.pop(l).to(device, non_blocking=True)

    return g
    
def load_model(run):
    """
        Load full trained model with id `run`

    """

    meta = pickle.load(open(f'static/models/{run}/meta.p', 'rb'))

    edge_map = meta['edge_map']
    num_edge_types = len(edge_map)

    model_dict = torch.load(f'static/models/{run}/{run}.pth', map_location='cpu')
    model = Model(dims=meta['embedding_dims'], attributor_dims=meta['attributor_dims'], num_rels=num_edge_types,
                  num_bases=-1,
                  device='cpu',
                  pool=meta['pool'])
    model.load_state_dict(model_dict['model_state_dict'])
    return model, meta

def inference_on_graph(model, graph, edge_map, device='cpu'):
    """
        Do inference on one networkx graph.
    """
    graph_nx = graph.to_undirected()
    one_hot = {edge: torch.tensor(edge_map[label]) for edge, label in
               (nx.get_edge_attributes(graph_nx, 'label')).items()}
    one_hot_nucs  = {node: torch.tensor(nuc_map[label], dtype=torch.float32) for node, label in
               (nx.get_node_attributes(graph_nx, 'nuc')).items()}

    nx.set_edge_attributes(graph_nx, name='one_hot', values=one_hot)
    nx.set_node_attributes(graph_nx, name='one_hot', values=one_hot_nucs)

    g_dgl = dgl.DGLGraph()
    g_dgl.from_networkx(nx_graph=graph_nx, node_attrs=['one_hot'], edge_attrs=['one_hot'])
    graph_ready = send_graph_to_device(g_dgl, device)

    return model(graph_ready)
