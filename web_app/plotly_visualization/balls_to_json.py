from balls_generation.files_utils import read_balls_file
import numpy as np
from nltk.corpus import wordnet as wn


class Ball:

    def __init__(self, word_, definition_, radius_, vector_):
        self.word = word_
        self.definition = definition_
        self.radius = radius_
        self.vector = vector_

    def __repr__(self):
        return f"({self.word}, {self.definition}, {self.radius}, {self.vector})"


def balls_to_object(path):
    circles_dic = {}
    read_balls_file(path, circles_dic)

    words = list(circles_dic.keys())
    radius = [values[-1] for values in circles_dic.values()]
    vectors = [np.multiply(np.array(values[:2]), values[-2]) for values in circles_dic.values()]

    out = list()
    for i in range(len(words)):
        # word_wn = wn.synset(words[i])
        # definition = word_wn.definition()
        definition = "Definition"

        out.append(Ball(words[i], definition, float(radius[i]), vectors[i].tolist()))

    return out


def balls_to_json(path):
    circles_dic = {}
    read_balls_file(path, circles_dic)

    words = list(circles_dic.keys())
    radius = [values[-1] for values in circles_dic.values()]
    vectors = [np.multiply(np.array(values[:2]), values[-2]) for values in circles_dic.values()]

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


    # print(json_balls)
    return out


if __name__ == '__main__':
    BALLS_PATH = "../out/test1/reduced_nballs_after.txt"
    print(balls_to_object(BALLS_PATH))
