from enum import Enum
import random

import matplotlib.pyplot as plt
import numpy as np
import math

from matplotlib import pyplot
from matplotlib.patches import Circle


class Operation(Enum):
    INITIALIZE = 0
    SEPERATE = 1
    CONTAIN = 2


class NBall:
    def __init__(self, vector):
        self.vector = vector


class DebugCircle:
    def __init__(self, vector, radius):
        self.vector = vector
        self.radius = radius
        self.first_sibling = False

def get_parent(root, childDict):
    for key, value in childDict.items():
        if root in value:
            return key
    return None



def get_siblings(root, childDict):
    out = childDict[get_parent(root, childDict)]
    out = [x for i, x in enumerate(out) if x != root]
    return out

def log_processing(ball_generation_log, childrenDic):
    print(childrenDic)
    [print(log) for log in ball_generation_log]
    circles = {}
    for log in ball_generation_log:
        if log["operation"] == Operation.INITIALIZE:
            if not circles:
                circles[log["key"]] = DebugCircle(np.array([0,0]), 1)
                circles[log["key"]].first_sibling = True
                continue
            siblings = get_siblings(log["key"], childrenDic)
            if any([i in circles for i in siblings]):
                print(siblings)
                siblings = [s for s in siblings if s in circles.keys()]
                ref = circles[[s for s in siblings if circles[s].first_sibling][0]]
                number = sum([i in circles for i in siblings])
                total = len(siblings)
                phi = number/total * 2 * np.pi
                x = 3 * np.cos(phi) + ref.vector[0]
                y = 3 * np.sin(phi) + ref.vector[1]
                circles[log["key"]] = DebugCircle(np.array([x, y]), 1)

            else:
                ref_circle = circles[list(circles.keys())[-1]]
                circles[log["key"]] = DebugCircle(np.array([ref_circle.vector[0] + 3, 0]), 1)
                circles[log["key"]].first_sibling = True



            print("key", log["key"], "parent", get_parent(log["key"], childrenDic))
            print("key", log["key"], "siblings", get_siblings(log["key"], childrenDic))
            pass
        elif log["operation"] == Operation.CONTAIN:
            pass
        elif log["operation"] == Operation.SEPERATE:
            pass

    vectors = []
    radii = []
    words = []
    for key, value in circles.items():
        vectors.append(value.vector)
        radii.append(value.radius)
        words.append(key)
    plot(vectors, radii, words)

def plot_operation():
    circle1 = plt.Circle((0, 0), 0.2, color='r')
    circle2 = plt.Circle((0.5, 0.5), 0.2, color='blue')
    circle3 = plt.Circle((1, 1), 0.2, color='g', clip_on=False)

    fig, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
    # (or if you have an existing figure)
    # fig = plt.gcf()
    # ax = fig.gca()

    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)

    fig.savefig('plotcircles.png')


def random_point(xy, r):
    r = float(r)
    theta = random.random() * 2 * math.pi
    return xy[0] + math.cos(theta) * r, xy[1] + math.sin(theta) * r


def plot(vectors, radius, words):
    fig, ax = pyplot.subplots()
    fig.suptitle("test", fontsize=20)
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(vectors))]

    for i, vector in enumerate(np.array(vectors)):
        e = Circle(xy=vector, radius=float(radius[i]),linewidth=1.)
        ax.add_artist(e)
        e.set_edgecolor(colors[i])
        e.set_facecolor('none')

    x = [i[0] for i in vectors]
    y = [i[1] for i in vectors]
    max_radius = max(radius)
    if max_radius < 1:
        max_radius = 1
    margin = 1.2 * max_radius
    ax.set_xlim([min(x) - margin, max(x) + margin])
    ax.set_ylim([min(y) - margin, max(y) + margin])
    ax.set_aspect(1)

    for i, word in enumerate(words):
        point = random_point(vectors[i], radius[i])
        ax.text(point[0], point[1], '%s' % (str(word)), size=10, zorder=1, color=colors[i])
    fig.show()
    plt.show()


def plot_dic(circles_dic, figure_title, filtered_words=[]):
    fig, ax = pyplot.subplots()
    fig.suptitle(figure_title, fontsize=20)
    if len(filtered_words) > 0:
        circles_dic = {k: circles_dic[k] for k in filtered_words if k in circles_dic}
    words = list(circles_dic.keys())
    radius = [values[-1] for values in circles_dic.values()]
    vectors = [np.multiply(np.array(values[:2]), values[-2]) for values in circles_dic.values()]
    plot(vectors, radius, words, fig, ax)
    fig.savefig(figure_title+".svg")