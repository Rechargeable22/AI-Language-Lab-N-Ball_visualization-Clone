import os
from utils.files_utils import *
from visualization.dimensions_utils import reduce_dimensions
from visualization.checker import check_all_tree
from visualization.transformation_2d import fix_one_family

def reduce_and_fix(balls_file_path, children_file_path, output):
    output_file_path, output_file_ext = os.path.splitext(output)
    output_file_before = output_file_path + "_before" + output_file_ext
    output_file_after = output_file_path + "_after" + output_file_ext
    children_dic = {}
    balls_dic = {}
    read_balls_file(balls_file_path, balls_dic)
    read_children_file(children_file_path, children_dic)
    circles_dic = reduce_dimensions(balls_dic)
    print("\nBalls reduced to circles successfully\n")
    check_all_tree(balls_dic, children_dic, "N-Balls")
    check_all_tree(circles_dic, children_dic, "2D circles before fixing")
    save_data(output_file_before, circles_dic)
    fix_one_family("*root*", circles_dic, children_dic, balls_dic)
    check_all_tree(circles_dic, children_dic, "2D circles after fixing")
    save_data(output_file_after, circles_dic)