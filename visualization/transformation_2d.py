import itertools
from visualization.vectors_utils_2d import *

ALPHA = 0.000000000001

def magic_scaling(word, circles_dic, children_dic, root, scale_factor):
    children = children_dic[word]
    circles_dic[word][-1] = abs(circles_dic[word][-1] * scale_factor)
    if word != root:
        word_center = get_coordinates(word, circles_dic)
        root_center = get_coordinates(root, circles_dic)
        delta = scale_factor * (word_center[0] - root_center[0]), scale_factor * (word_center[1] - root_center[1])
        new_center = root_center[0] + delta[0], root_center[1] + delta[1]
        new_vector, new_length = get_vector_and_length(new_center)
        circles_dic[word][: -2] = new_vector
        circles_dic[word][-2] = new_length
    if len(children) == 0:
        return
    for child in children:
        magic_scaling(child, circles_dic, children_dic, root, scale_factor)

def check_siblings(word1, word2, circles_dic, children_dic, parent, scale_factor):
    siblings_for_word1_and_word2 = children_dic[parent]
    for sibling in siblings_for_word1_and_word2:
        if sibling != word1 and sibling != word2:
            disjoint_with_word1 = disjoint_degree(circles_dic[word1], circles_dic[sibling])
            disjoint_with_word2 = disjoint_degree(circles_dic[word2], circles_dic[sibling])
            if disjoint_with_word1 < ALPHA or disjoint_with_word2 < ALPHA:
                magic_scaling(sibling, circles_dic, children_dic, sibling, scale_factor)

def disjoint_circles_by_scaling_down(word1, word2, circles_dic, children_dic, parent):
    old_radius1 = circles_dic[word1][-1]
    old_radius2 = circles_dic[word2][-1]
    dis = dis_between_circles_centers(circles_dic[word1], circles_dic[word2])
    dis = (dis - (dis * 0.01))
    scale_factor = dis / (old_radius1 + old_radius2)
    check_siblings(word1, word2, circles_dic, children_dic, parent, scale_factor)
    magic_scaling(word1, circles_dic, children_dic, word1, scale_factor)
    magic_scaling(word2, circles_dic, children_dic, word2, scale_factor)

def contain_circles(child, parent, circles_dic, children_dic):
    if circles_dic[child][-1] == 0:
        return
    dis = dis_between_circles_centers(circles_dic[child], circles_dic[parent])
    dis = (dis + (dis * 0.05))
    if is_circles_disjoint(circles_dic[child], circles_dic[parent]):
        scale_factor = (circles_dic[child][-1] + dis) / circles_dic[parent][-1]
        circles_dic[parent][-1] = abs(circles_dic[parent][-1] * scale_factor)
    else:
        scale_factor = (circles_dic[parent][-1] - dis) / circles_dic[child][-1]
        magic_scaling(child, circles_dic, children_dic, child, scale_factor)

def fix_one_family(word, circles_dic, children_dic, balls_dic):
    children = children_dic[word]
    if len(children) == 0:
        return
    for child in children:
        fix_one_family(child, circles_dic, children_dic, balls_dic)
    if len(children) > 1:
        for child1, child2 in itertools.combinations(children, 2):
            if not is_circles_disjoint(circles_dic[child1], circles_dic[child2]) and \
                    is_circles_disjoint(balls_dic[child1], balls_dic[child2]):
                disjoint_circles_by_scaling_down(child1, child2, circles_dic, children_dic, word)
    if word == "*root*":
        return
    for child in children:
        if not is_circle2_contains_circle1(circles_dic[child], circles_dic[word]) and \
                is_circle2_contains_circle1(balls_dic[child], balls_dic[word]):
            contain_circles(child, word, circles_dic, children_dic)
