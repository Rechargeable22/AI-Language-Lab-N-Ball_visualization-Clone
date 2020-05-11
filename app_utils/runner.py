import sys
import argparse

import app_utils.fetch_glove_model
from balls_generation import main as m
from app_utils.web_input_parsing import input_text_to_path


def run(ext_args=None, input_words=None, debug_circles_list=None):
    print(sys.argv)
    parser = argparse.ArgumentParser(description="Installation and configuration of Natlink and its dependency")
    parser.add_argument('--no_balls', dest='generate_balls', action='store_false')
    parser.add_argument('--no_dimension_reduction', dest='dimension_reduction', action='store_false')
    parser.add_argument('--no_visualize_nballs', dest='visualize_nballs', action='store_false')
    parser.add_argument('--outfolder_path', default="out/test")
    parser.set_defaults(generate_balls=True)
    parser.set_defaults(dimension_reduction=True)
    parser.set_defaults(visualize_nballs=False)

    args = None
    if ext_args:
        args = parser.parse_args(ext_args.split())
    else:
        args = parser.parse_args()

    # What part we run
    generate_balls = args.generate_balls
    reduce_dimensionality = args.dimension_reduction
    visualize_nballs = args.visualize_nballs
    outfolder_path = args.outfolder_path

    word_embedding = "res/glove.6B.50d.txt"

    app_utils.fetch_glove_model.fetch_glove()
    print(args)
    if generate_balls:
        m.main(f" --generate_nballs  --w2v {word_embedding} --output {outfolder_path}".split(), input_words, debug_circles_list)

    BALLS_FILE_PATH = f"{outfolder_path}/nballs.txt"
    CHILDREN_FILE_PATH = f"{outfolder_path}/children.txt"
    OUTPUT_FILE_PATH = f"{outfolder_path}/reduced_nballs.txt"

    if reduce_dimensionality:
        m.main((f"--reduceAndFix --balls {BALLS_FILE_PATH} --children {CHILDREN_FILE_PATH} \
        --output_path {OUTPUT_FILE_PATH}").split())

    CIRCLES_FILE_PATH = OUTPUT_FILE_PATH
    WORDS_FILE_PATH = None

    if visualize_nballs:
        m.main(f" --vis --circles {CIRCLES_FILE_PATH}".split())


if __name__ == "__main__":
    output = []
    # run("", input_text_to_path(
    #     "human is animal, "),
    #     output)
    run(" --no_visualize_nballs --outfolder_path out/random", input_text_to_path("duck is animal, dog is animal, chicken is animal,human is animal, socrates is human, kant is human, wolf is animal, tank is not animal, flower is plant, rose is flower, tulp is flower"), output)
    print(output)
