import json
from nltk.corpus import wordnet as wn
import utils.plotly as util

import runner as r



def background_ball_generation(input_words):
    with open("../res/sample_input.txt", "w") as file:
        [file.write(word + "\n") for word in input_words]

    # r.run("--no_visualize_nballs")

    word_senses = {}
    word_definitions = {}
    for word in input_words:
        word_wn = wn.synsets(word)
        word_senses[word] = [w.name() for w in word_wn]
        word_definitions[word] = [w.definition() for w in word_wn]

    out = {"input_words": input_words, "word_senses": word_senses, "word_definitions": word_definitions,
           "plotly_json": util.plot_balls()}
    out = json.dumps(out)

    return out