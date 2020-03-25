from utils.files_utils import read_balls_file
import numpy as np
import json
from nltk.corpus import wordnet as wn


if __name__ == '__main__':
    BALLS_PATH = "../out/test1/reduced_nballs_after.txt"
    circles_dic_after = {}
    read_balls_file(BALLS_PATH, circles_dic_after)

    words = list(circles_dic_after.keys())
    radius = [values[-1] for values in circles_dic_after.values()]
    vectors = [np.multiply(np.array(values[:2]), values[-2]) for values in circles_dic_after.values()]

    out = list()
    for i in range(len(words)):
        item = dict()

        word_wn = wn.synset(words[i])
        definition = word_wn.definition()

        item["word"] = words[i]
        item["definition"] = definition
        item["radius"] = float(radius[i])
        item["vector"] = vectors[i].tolist()

        out.append(item)

    print(json.dumps(out))