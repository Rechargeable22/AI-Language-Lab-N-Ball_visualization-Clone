import plotly.graph_objects as go
from igraph import Graph, EdgeSeq

from utils.files_utils import read_word_path


def combined_tree_paths_fig(input_list, file_path):
    paths = read_word_path(file_path)
    if "*root*" in paths:
        del paths["*root*"]

    tree = Graph(directed=True)

    edges = []
    nodes = []

    edges, nodes = nodes_edges_calculation(edges, input_list, nodes, paths, tree)

    nr_vertices = len(edges) + 1
    lay = tree.layout('rt')
    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    max_y = max(Y)

    edges_list = [e.tuple for e in tree.es]

    L = len(position)
    y_nodes = [position[k][0] for k in range(L)]
    x_nodes = [(2 * max_y - position[k][1]) * -1 for k in range(L)]
    y_edge = []
    x_edge = []
    for edge in edges_list:
        y_edge += [position[edge[0]][0], position[edge[1]][0], None]
        x_edge += [(2 * max_y - position[edge[0]][1]) * -1, (2 * max_y - position[edge[1]][1]) * -1, None]

    labels = nodes

    fig = go.Figure()
    plot_fig(fig, labels, x_edge, x_nodes, y_edge, y_nodes)

    return fig


def nodes_edges_calculation(edges, input_list, nodes, paths, tree):
    for input_key in input_list:
        data = paths.get(input_key, "")
        for i in range(len(data)):
            if i != len(data) - 1:
                edges.append((data[i], data[i + 1]))
            nodes.append(data[i])
    edges = list(dict.fromkeys(edges))
    nodes = list(dict.fromkeys(nodes))
    for n in nodes:
        tree.add_vertices(n)
    for e in edges:
        tree.add_edge(e[0], e[1])
    return edges, nodes


def plot_fig(fig, labels, x_edge, x_nodes, y_edge, y_nodes):
    fig.add_trace(go.Scatter(x=x_edge,
                             y=y_edge,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=x_nodes,
                             y=y_nodes,
                             mode="markers+text",
                             text=labels,
                             textposition="top center",
                             hoverinfo='none',
                             marker_symbol='circle',
                             marker_line_color='steelblue',
                             line_color='steelblue',
                             marker_color='steelblue',
                             marker_line_width=3,
                             marker_size=15,
                             textfont_size=12,
                             textfont_family='Roboto, sans-serif',
                             ))
    # arrows = []
    # arrow_spacing = 0.1
    # for i in range(len(nodes) - 1):
    #     arrow_generation(arrow_spacing, 0.0, 0, arrows, i, i + 1, x_nodes, y_nodes)
    #
    fig.update_layout(
        # annotations=arrows,
        xaxis=dict(
            # range=[-0.40, nodes_no - 1 + 0.40],
            showline=False,
            showgrid=False,
            showticklabels=False,
        ),
        yaxis=dict(
            # range=[-1, 0],
            showline=False,
            showgrid=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0,
        ),
    )
