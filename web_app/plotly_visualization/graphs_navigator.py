import web_app.plotly_visualization.balls_graph as balls_graph
import json
import plotly

from web_app.plotly_visualization.animation_graph_v2 import animation_graph_plot2
from web_app.plotly_visualization.tree_forest_graph import path_tree_forest
import web_app.plotly_visualization.balls_to_json as util


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
    balls = util.balls_to_object(f"{outfolder_path}/reduced_nballs_after.txt")
    return balls_graph.plot_balls(balls)

def plot_animation(list):
    fig= animation_graph_plot2(list, 1)

    fig.show(config={'scrollZoom': True, 'displayModeBar': False})
    return "animation"

def plot_animation_json(debug_steps):
    output=[]
    for i,v in enumerate(debug_steps):
        print(v)
        serialized = balls_graph.plot_balls([a for k, a in v.items()])
        output.append(serialized)
    return output