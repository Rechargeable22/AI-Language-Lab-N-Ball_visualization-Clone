import json
import os
import random

import plotly_visualization.graphs_navigator as util

from app_utils import runner as r


def background_ball_generation(input_words):
    outfolder_name = random.randint(0, 1000000)
    outfolder_path = f"out/{outfolder_name}"
    if not os.path.isdir(outfolder_path):
        os.mkdir(outfolder_path)

    debug_circles_list = []
    r.run(f"--no_visualize_nballs --outfolder_path {outfolder_path}", input_words, debug_circles_list)

    log = [dcl["log"] for dcl in debug_circles_list]
    debug_circles_list = [dcl["circles"] for dcl in debug_circles_list]
    print(debug_circles_list)

    input_words = input_words
    word_senses_cumulative = input_words  # hack me

    out = {
        "plotly_json": util.plot_balls(outfolder_path),
        "plotly_full_tree": util.plot_combined_tree_json(word_senses_cumulative, outfolder_path),
        "plotly_animation": util.plot_animation_json(debug_circles_list),
        "generation_log": log}
    out = json.dumps(out)

    return out
