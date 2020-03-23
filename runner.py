import os, sys
import argparse

import utils.google_fetch
import main as m


def run(ext_args=None):
    print(sys.argv)
    parser = argparse.ArgumentParser(description="Installation and configuration of Natlink and its dependency")
    parser.add_argument('--no_balls', dest='generate_balls', action='store_false')
    parser.add_argument('--no_dimension_reduction', dest='dimension_reduction', action='store_false')
    parser.add_argument('--no_visualize_nballs', dest='visualize_nballs', action='store_false')
    parser.set_defaults(generate_balls=True)
    parser.set_defaults(dimension_reduction=True)
    parser.set_defaults(visualize_nballs=True)

    args=None
    if ext_args:
        args = parser.parse_args(ext_args.split())
    else:
        args = parser.parse_args()



    # What part we run
    generate_balls = args.generate_balls
    reduce_dimensionality = args.dimension_reduction
    visualize_nballs = args.visualize_nballs


    word_embedding = "res/glove.6B.50d.txt"
    words = "res/sample_input.txt"

    utils.google_fetch.fetch_glove()

    if generate_balls:
        m.main((f" --generate_nballs --input {words} --w2v {word_embedding} --output out/test1").split())

    BALLS_FILE_PATH = "out/test1/nballs.txt"
    CHILDREN_FILE_PATH = "out/test1/children.txt"
    OUTPUT_FILE_PATH = "out/test1/reduced_nballs.txt"

    if reduce_dimensionality:
        m.main((f"--reduceAndFix --balls {BALLS_FILE_PATH} --children {CHILDREN_FILE_PATH} \
        --output_path {OUTPUT_FILE_PATH}").split())

    CIRCLES_FILE_PATH = OUTPUT_FILE_PATH
    WORDS_FILE_PATH = None

    if visualize_nballs:
        m.main(f" --vis --circles {CIRCLES_FILE_PATH}".split())

if __name__ == "__main__":
    run()