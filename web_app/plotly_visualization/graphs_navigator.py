import web_app.plotly_visualization.balls_graph as balls_graph
import json
import plotly

from web_app.plotly_visualization.tree_forest_graph import plot_path_tree_forest
import web_app.plotly_visualization.balls_converter as util


def plot_combined_tree_json(input_list, path):
    """
    Takes a tree-structure and calls function to generate the graph of forest of words-paths-trees and parse it to json.
    See :func:'plot_path_tree_forest.tree_forest_graph.plotly_visualization.web_app''

    :param input_list: list of input key words
    :param path: path to the file of a list of str of key words and its paths words saparated by a spaces

    :return: Serialized JSON formatted ''str'' of plot showing words tree forest
    """

    input_list = [element.split()[0] for element in input_list][1:]
    fig = plot_path_tree_forest(input_list, path + "/small.wordSensePath.txt")
    serialized = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return serialized


def plot_balls_json(outfolder_path):
    """
    Takes path of file with output balls and pass it to the function to convert balls into the Ball objects. See :func:'balls_to_object.balls_wrapper.plotly_visualization.web_app'
    Calls function :func:'plot_balls.balls_graph.plotly_visualization.web_app' to create the graph.

    :param outfolder_path: path to the file of a balls with their key word, coordinates and radius

    :return: Serialized JSON formatted ''str'' of plot showing balls-structured tree
    """

    balls = util.balls_to_object(f"{outfolder_path}/reduced_nballs_after.txt")
    return balls_graph.plot_balls(balls)


def plot_animation_json(debug_steps):
    """
    Enumarates through the list of the steps of the algorithm which creates the balls-tree structures and generates json serialized plot for every step. See :func:'plot_balls.balls_graph.plotly_visualization.web_app'.

    :param debug_steps: List of the steps which contain list of the balls with its key word, coordinates and radius

    :return: List of serialized JSON formatted ''str'' of plots showing each steps how the ball-tree structure was created
    """
    output = []
    for i, v in enumerate(debug_steps):
        serialized = balls_graph.plot_balls([a for k, a in v.items()])
        output.append(serialized)
    return output
