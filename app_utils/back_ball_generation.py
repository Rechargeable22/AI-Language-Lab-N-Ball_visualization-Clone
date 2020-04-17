import json
import os
import random

import plotly_visualization.plotly as util

from app_utils import runner as r


def background_ball_generation(input_words):
    outfolder_name = random.randint(0, 1000000)
    # outfolder_name = 308752
    outfolder_path = f"out/{outfolder_name}"
    if not os.path.isdir(outfolder_path):
        os.mkdir(outfolder_path)
    r.run(f"--no_visualize_nballs --outfolder_path {outfolder_path}", input_words)


    word_senses = {}
    word_definitions = {}
    word_path_fig = {}
    input_words = input_words
    word_senses_cumulative = []
    word_senses_cumulative = input_words # hack me
    # for word in input_words:
    #     word_wn = wn.synsets(word)
    #     word_senses[word] = [w.name() for w in word_wn]
    #     word_definitions[word] = [w.definition() for w in word_wn]
    #     word_senses_cumulative.extend([w.name() for w in word_wn])
    #
    #     word_path_fig[word] = [util.tree_path_json(sense.name(), outfolder_path) for sense in word_wn]

    out = {
           # "input_words": input_words,
           # "word_senses": word_senses,
           # "word_definitions": word_definitions,
           # "word_path_fig": word_path_fig,
           "plotly_json": util.plot_balls(outfolder_path),
           "plotly_full_tree": util.plot_combined_tree_json(word_senses_cumulative, outfolder_path)}
    out = json.dumps(out)

    return out
