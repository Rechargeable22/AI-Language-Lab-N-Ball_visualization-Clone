import web_app.plotly_visualization.balls_graph as balls_graph
import json
import plotly

from web_app.plotly_visualization.tree_forest_graph import plot_path_tree_forest
import web_app.plotly_visualization.balls_wrapper as util


def plot_combined_tree_json(input_list, path):
    input_list = [element.split()[0] for element in input_list][1:]
    fig = plot_path_tree_forest(input_list, path + "/small.wordSensePath.txt")
    serialized = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return serialized


def plot_balls_json(outfolder_path):
    balls = util.balls_to_object(f"{outfolder_path}/reduced_nballs_after.txt")
    return balls_graph.plot_balls(balls)


def plot_animation_json(debug_steps):
    output = []
    for i, v in enumerate(debug_steps):
        serialized = balls_graph.plot_balls([a for k, a in v.items()])
        output.append(serialized)
    return output
