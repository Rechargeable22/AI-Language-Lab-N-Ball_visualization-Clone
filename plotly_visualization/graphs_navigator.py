import plotly_visualization.balls_graph as balls_graph
import json
import plotly

from plotly_visualization.animation_graph import animation_graph_plot
from plotly_visualization.animation_graph_v2 import animation_graph_plot2
from plotly_visualization.tree_forest_graph import path_tree_forest


def plot_combined_tree_path(input_list):
    fig = path_tree_forest(input_list, "out/test1/small.wordSensePath.txt")
    fig.show()
    return ""


def plot_combined_tree_json(input_list, path):
    print(input_list)
    input_list = [element.split()[0] for element in input_list][1:]
    print(input_list)

    fig = path_tree_forest(input_list, path + "/small.wordSensePath.txt")
    serialized = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return serialized


def plot_balls(outfolder_path):
    return balls_graph.plot_balls(outfolder_path)

def plot_animation(list):
    fig= animation_graph_plot2(list, 1)

    fig.show(config={'scrollZoom': True, 'displayModeBar': False})
    return "animation"

def plot_animation_json(list):
    fig= animation_graph_plot2(list, 1)
    serialized = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return serialized