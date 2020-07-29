import plotly.graph_objects as go
from igraph import Graph

from balls_generation.files_utils import read_word_path


def plot_path_tree_forest(input_list, file_path):
    """
    Reads a tree-structure file.
    Calls function func:'nodes_edges_calculation.tree_forest_graph.plotly_visualization.web_app' to generate the graph of edges and nodes of words-paths-trees using igraph library.
    Converts generated graph to coordinates ''x'' and ''y'' for every node and every edge.
    Generates list of labels for every node.
    Calls function func;'plot_fig' to  plot the graph.

    :param input_list: list of input key words
    :param file_path: path to the file of a list of str of key words and its paths words saparated by a spaces

    :return: plotly figure
    """

    paths = read_word_path(file_path)
    if "*root*" in paths:
        del paths["*root*"]

    tree = Graph(directed=True)

    edges = []
    nodes = []

    edges, nodes = nodes_edges_calculation(edges, input_list, nodes, paths, tree)

    for n in nodes:
        if n == '*root*':
            del nodes[nodes.index(n)]

    nr_vertices = len(edges) + 1
    lay = tree.layout('rt')
    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    max_y = max(Y)

    edges_list = [e.tuple for e in tree.es]

    L = len(position)
    y_nodes = [position[k][0] for k in range(L)]
    y_nodes.pop(0)
    x_nodes = [(2 * max_y - position[k][1]) * -1 for k in range(L)]
    x_nodes.pop(0)
    y_edge = []
    x_edge = []

    for e in edges_list:
        if e[0] == 0:
            del edges_list[edges_list.index(e)]
    for edge in edges_list:
        y_edge += [(position[edge[0]][0], position[edge[1]][0])]
        x_edge += [((2 * max_y - position[edge[0]][1]) * -1, (2 * max_y - position[edge[1]][1]) * -1)]

    labels = nodes
    x_smallest = 0
    x_biggest = 0
    y_smallest = 0
    y_biggest = 0

    for p in range(len(x_nodes)):
        if x_nodes[p] < x_smallest:
            x_smallest = x_nodes[p]
        if x_nodes[p] > x_biggest:
            x_biggest = x_nodes[p]
        if y_nodes[p] < y_smallest:
            y_smallest = y_nodes[p]
        if y_nodes[p] > y_biggest:
            y_biggest = y_nodes[p]

    x_range = x_biggest - x_smallest
    y_range = y_biggest - y_smallest
    if y_range < 1:
        y_range = 1
    if x_range < 1:
        x_range = 1
    axis_ratio = float(x_range) / float(y_range)

    fig = go.Figure()
    plot_fig(fig, labels, x_edge, x_nodes, y_edge, y_nodes, axis_ratio)

    return fig


def nodes_edges_calculation(edges, input_list, nodes, paths, tree):
    """
    Converts the input keys and data from file, consisting list of paths, to the lists of edges and nodes and adds it to the graph created by igraph library.

    :param tree: tree created using igraph library
    :param paths: list of paths for the key words extracted from the file
    :param nodes: empty list for nodes
    :param edges: empty list for edges
    :param input_list: list of input key words

    :return: edges: edges of the tree
    :return: nodes: nodes of the tree
    """

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


def arrow_generation(arrow_spacing_x, arrows, i, x_axis, y_axis):
    """
    Generate the edge for the graph as a plotly annotation arrow.

    :param y_axis: list of ''x'' coordinate for every node
    :param x_axis:  list of ''y'' coordinate for every node
    :param i: index of the current processed node
    :param arrows: list of arrows to which generated arrow is added
    :param arrow_spacing_x: spacing between the arrow and node for coordinate ''x''
    """

    arrows.append(dict(
        ax=x_axis[i][0] + arrow_spacing_x,
        ay=y_axis[i][0],
        axref='x',
        ayref='y',
        x=x_axis[i][1] - arrow_spacing_x,
        y=y_axis[i][1],
        xref='x',
        yref='y',
        textangle=0,
        arrowcolor="steelblue",
        arrowsize=1,
        arrowwidth=3,
        arrowhead=1,
    )
    )


def plot_fig(fig, labels, x_edge, x_nodes, y_edge, y_nodes, ratio):
    """
    Plots the plotly graph of the forest of trees. Adds all the traces(nodes), annotations(arrows) and layout to the plot.

    :param fig: empty plotly figure
    :param labels: list of labels for the nodes
    :param x_edge: list of ''x'' coordinate for every edge
    :param x_nodes: list of ''x'' coordinate for every node
    :param y_edge: list of ''y'' coordinate for every edge
    :param y_nodes: list of ''y'' coordinate for every node
    :param ratio: ratio to scale the figure properly
    """
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

    arrows = []
    arrow_spacing = 0.1
    for i in range(len(x_edge)):
        arrow_generation(arrow_spacing, arrows, i, x_edge, y_edge)

    fig.update_layout(
        annotations=arrows,
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=False,
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1 - (1 / ratio),
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
