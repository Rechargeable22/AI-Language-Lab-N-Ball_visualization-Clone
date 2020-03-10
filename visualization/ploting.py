import os, random, math
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import pyplot
from utils.files_utils import *
from matplotlib.patches import Circle

def random_point(xy, r):
    r = float(r)
    theta = random.random() * 2 * math.pi
    return xy[0] + math.cos(theta) * r, xy[1] + math.sin(theta) * r


def plot(vectors, radius, words, fig, ax):
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(vectors))]
    for i, vector in enumerate(np.array(vectors)):
        e = Circle(xy=vector, radius=float(radius[i]))
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


def plot_dic(circles_dic, figure_title, filtered_words=[]):
    fig, ax = pyplot.subplots()
    fig.suptitle(figure_title, fontsize=20)
    if len(filtered_words) > 0:
        circles_dic = {k: circles_dic[k] for k in filtered_words if k in circles_dic}
    words = list(circles_dic.keys())
    radius = [values[-1] for values in circles_dic.values()]
    vectors = [np.multiply(np.array(values[:2]), values[-2]) for values in circles_dic.values()]
    plot(vectors, radius, words, fig, ax)


def visualize(circles_file_path, words_to_show_file_path):
    output_file_path, output_file_ext = os.path.splitext(circles_file_path)
    output_file_before = output_file_path + "_before" + output_file_ext
    output_file_after = output_file_path + "_after" + output_file_ext
    circles_dic_before = {}
    words_to_show = read_words_to_show_file(words_to_show_file_path)
    read_balls_file(output_file_before, circles_dic_before)
    plot_dic(circles_dic_before, 'Circles before fixing', words_to_show)
    circles_dic_after = {}
    read_balls_file(output_file_after, circles_dic_after)
    plot_dic(circles_dic_after, 'Circles after fixing', words_to_show)
    plt.show()
