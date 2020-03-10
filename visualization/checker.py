import itertools
import json

from visualization.vectors_utils_2d import *


def check_one_level(word, circles_dic, children_dic, disjoint_failed=None, contained_failed=None):
    if contained_failed is None:
        contained_failed = {}
    if disjoint_failed is None:
        disjoint_failed = {}
    children = children_dic[word]
    disjoint_failed[word] = []
    contained_failed[word] = []
    if len(children) == 0:
        return
    for child in children:
        check_one_level(child, circles_dic, children_dic, disjoint_failed, contained_failed)
    if len(children) > 1:
        for child1, child2 in itertools.combinations(children, 2):
            is_disjoint = is_circles_disjoint(circles_dic[child1], circles_dic[child2])
            if not is_disjoint:
                disjoint_failed[word].append('{} {}'.format(child1, child2, word))
    if word != "*root*":
        for child in children:
            contained = is_circle2_contains_circle1(circles_dic[child], circles_dic[word])
            if not contained:
                contained_failed[word].append("{} {}".format(child, word))

def check_all_tree(circles_dic, children_dic, name="Tree"):
    disjoint_failed = {}
    contained_failed = {}
    check_one_level("*root*", circles_dic, children_dic, disjoint_failed, contained_failed)
    disjoint_failed = {k: v for k, v in disjoint_failed.items() if len(v) > 0}
    contained_failed = {k: v for k, v in contained_failed.items() if len(v) > 0}
    print("Checking {}".format(name))
    print("Disjoint Condition Failed Cases", json.dumps(disjoint_failed, indent=4, sort_keys=True))
    print("Contained Condition Failed Cases", json.dumps(contained_failed, indent=4, sort_keys=True))
    print("")