import numpy as np
import math


def get_coordinates_circle(circle):
    return np.multiply(circle[:-2], circle[-2])


def get_coordinates(word, circles_dic):
    return np.multiply(circles_dic[word][:-2], circles_dic[word][-2])


def get_vector_and_length(coordinates):
    magnitude = np.linalg.norm(coordinates)
    return [ele / magnitude for ele in coordinates], magnitude


def dis_between_circles_centers(circle1, circle2):
    if circle1 == circle2:
        return 0
    circle1_xy = get_coordinates_circle(circle1)
    circle2_xy = get_coordinates_circle(circle2)
    dis_sum = 0
    for i in range(len(circle1_xy)):
        dis_sum = dis_sum + pow(circle2_xy[i] - circle1_xy[i], 2)
    return math.sqrt(dis_sum)


def disjoint_degree(circle1, circle2):
    dis = dis_between_circles_centers(circle1, circle2)
    return dis - circle1[-1] - circle2[-1]


def is_circles_disjoint(circle1, circle2):
    degree = disjoint_degree(circle1, circle2)
    if degree < 0:
        return False
    return True


def containment_degree(circle1, circle2):
    dis = dis_between_circles_centers(circle1, circle2)
    return circle2[-1] - dis - circle1[-1]


def is_circle2_contains_circle1(circle1, circle2):
    degree = containment_degree(circle1, circle2)
    if degree < 0:
        return False
    return True
