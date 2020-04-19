import collections
import copy
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
    def __init__(self, vector, radius, text, color):
        self.vector = vector
        self.radius = radius
        self.first_sibling = False
        self.text = text
        self.color = color

    def __repr__(self):
        return f"DebugCircle((x:{self.vector[0]}, y:{self.vector[1]}), r:{self.radius})"


def get_parent(root, childDict):
    for key, value in childDict.items():
        if root in value:
            return key
    return None


def get_siblings(root, childDict):
    out = childDict[get_parent(root, childDict)]
    out = [x for i, x in enumerate(out) if x != root]
    return out


def gen_layer(node, left, right, dic):
    # generate circles for each layer of the source tree recursively
    children = dic[node]
    if children:
        if len(children) == 1:
            diameter_per_child = 0.8 * (right - left)
        else:
            diameter_per_child = (right - left) / len(children)
        circles = []
        if node != "*root*":
            color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            circles.append(DebugCircle(vector=np.array([(left + right) / 2, 0]), radius=(right - left) / 2, text=node, color=color))
        for i, child in enumerate(children):
            circles.append(gen_layer(child, left + i * diameter_per_child, left + (i + 1) * diameter_per_child, dic))
        return circles
    else:
        color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        return DebugCircle(vector=np.array([(left + right) / 2, 0]), radius=(right - left) / 2, text=node, color=color)


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable):
            for sub in flatten(el):
                yield sub
        else:
            yield el


def generate_perfect_circles(dic):
    # generates positions for circles in which they match the given tree structure perfectly
    circles = gen_layer(node="*root*", left=0., right=1., dic=dic)
    circles = list(flatten(circles))
    circle_dict = {}
    for c in circles:
        circle_dict[c.text] = c
    return circle_dict


class Log:
    def __init__(self, key, operation, operation_args, vector):
        self.key = key
        self.op = operation
        self.op_args = operation_args
        self.vec = vector

    def __repr__(self):
        return f"Log({self.key}, {self.op}, {self.op_args})"


def log_processing(ball_generation_log, childrenDic):
    print("\nLog processing")
    print("Children dic:", childrenDic)
    perfect_circles = generate_perfect_circles(childrenDic)
    print(perfect_circles)
    [print(log) for log in ball_generation_log]

    # (a,b) a falsely contains b and has to seperate it -> For all b we save a list of a's in which in falsely is e.g. dict[tank] = [plant, animal]
    overlap_pairs = [(log.key, arg) for log in ball_generation_log for arg in log.op_args if
                     log.op == Operation.SEPERATE]
    overlapping_circles = collections.defaultdict(list)
    for a, b in overlap_pairs:
        overlapping_circles[b].append(a)



    circles = {}
    for index, log in enumerate(ball_generation_log):
        if log.op == Operation.INITIALIZE:
            current = log.key

            if current in overlapping_circles:
                # TODO: initialize containing children
                circles_to_wrap = overlapping_circles[current] + [current]
                min_list = [perfect_circles[e].vector[0]-perfect_circles[e].radius for e in circles_to_wrap]
                min_x = min(min_list)
                max_list = [perfect_circles[e].vector[0]+perfect_circles[e].radius for e in circles_to_wrap]
                max_x = max(max_list)
                curr_vec = np.array([(min_x+max_x/2), 0])
                curr_radius = (max_x-min_x) / 2 * 1.0    # maybe we can make this stand out by multiplying with 0.9
                circles[current] = DebugCircle(curr_vec, curr_radius, current, color=perfect_circles[current].color)
                continue

            for l in ball_generation_log:
                if l.op_args and current in l.op_args:
                    other = l.key
                    curr_vec = perfect_circles[other].vector + (np.random.random_sample((2,)) - 0.5) * perfect_circles[
                        other].radius
                    curr_radius = perfect_circles[other].radius
                    circles[current] = DebugCircle(curr_vec, curr_radius, log.key, color=perfect_circles[current].color)
                elif len(childrenDic[current]) > 0:
                    children = childrenDic[current]
                    children_vecs = [perfect_circles[c].vector for c in children]
                    curr_vec = np.average([children_vecs], axis=1).flatten()
                    curr_radius = perfect_circles[children[0]].radius
                    circles[current] = DebugCircle(curr_vec, curr_radius, log.key, color=perfect_circles[current].color)
                else:
                    circles[current] = copy.deepcopy(perfect_circles[current])
        elif log.op == Operation.CONTAIN:
            circles[current] = copy.deepcopy(perfect_circles[current])
        elif log.op == Operation.SEPERATE:
            current = log.key       # current stays the same, we kick out other.
            other = log.op_args[0]   # elment to be seperated from current; not sure about [0]
            if other in overlapping_circles:
                overlapping_circles[other].remove(current)
                # calculate position of other
                if overlapping_circles[other]:
                    # still contains elements, compute cover for them
                    min_list = [perfect_circles[e].vector[0] - perfect_circles[e].radius for e in overlapping_circles[other]]
                    min_x = min(min_list)
                    max_list = [perfect_circles[e].vector[0] + perfect_circles[e].radius for e in overlapping_circles[other]]
                    max_x = max(max_list)
                    other_vec = np.array([(min_x + max_x)/2, 0])
                    other_radius = (max_x - min_x) / 2 * 1.0  # maybe we can make this stand out by multiplying with 0.9
                    circles[other] = DebugCircle(other_vec, other_radius, other, color=perfect_circles[other].color)
                else:
                    # set other circle to the perfect circle
                    del(overlapping_circles[other])
                    circles[other] = copy.deepcopy(perfect_circles[other])

        # draw circles
        plot_circles(circles)


def plot_circles(circles):
    vectors = []
    radii = []
    words = []
    colors = []
    for key, value in circles.items():
        vectors.append(value.vector)
        radii.append(value.radius)
        words.append(key)
        colors.append(value.color)

    # for k, c in perfect_circles.items():
    #     vectors.append(c.vector)
    #     radii.append(c.radius)
    #     words.append(c.text)
    plot(vectors, radii, words, colors)


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
    return xy[0] - 0.2 * r, xy[1] - 1.2 * r


def plot(vectors, radius, words, colors):
    fig, ax = pyplot.subplots()
    fig.suptitle("NBalls in 2D", fontsize=20)
    # colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(vectors))]

    for i, vector in enumerate(np.array(vectors)):
        e = Circle(xy=vector, radius=float(radius[i]), linewidth=1.)
        ax.add_artist(e)
        e.set_edgecolor(colors[i])
        e.set_facecolor('none')

    x = [i[0] for i in vectors]
    y = [i[1] for i in vectors]
    max_radius = max(radius)
    if max_radius < 1:
        max_radius = 1
    margin = 1.2 * max_radius
    # ax.set_xlim([min(x) - margin, max(x) + margin])
    # ax.set_ylim([min(y) - margin, max(y) + margin])
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.55, 0.55)
    ax.set_aspect(1)

    for i, word in enumerate(words):
        point = random_point(vectors[i], radius[i])
        ax.text(point[0], point[1], '%s' % (str(word)), size=10, zorder=1, color=colors[i])
    fig.show()
    fig.savefig("Perfect circles.svg")
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
    fig.savefig(figure_title + ".svg")
