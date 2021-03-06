import argparse

import web_app.Fetch_glove_model
from balls_generation import main as m


def run(ext_args: str = None, input_words: str = None, debug_circles_list: list = None) -> None:
    """
    Translates the CLI of the N-Ball generation to a python callable interface. Takes a tree-structure
    and generates corresponding output files see  :func:'balls_generation.main.main'

    :param ext_args: comma separated CLI arguments as str, see :func:'balls_generation.main.main'
    :param input_words: str of input tree structure that is used to generate the N-Balls, see ReadMe#String Tree-Structure
    :param debug_circles_list: should pass empty list which will be filled with debug steps of the N-Ball generation.
    Unlike other returns that are written to disk we opted to keep this additional output in memory

    :return: Returns are not explicit but rather on files and in debug_circles
    """

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

    # See which parts we actually need to run
    generate_balls = args.generate_balls
    reduce_dimensionality = args.dimension_reduction
    visualize_nballs = args.visualize_nballs
    outfolder_path = args.outfolder_path

    # default word-embedding used for N-Ball
    word_embedding = "res/glove.6B.50d.txt"
    web_app.Fetch_glove_model.fetch_glove()

    if generate_balls:
        m.main(f" --generate_nballs  --w2v {word_embedding} --output {outfolder_path}".split(), input_words,
               debug_circles_list)

    BALLS_FILE_PATH = f"{outfolder_path}/nballs.txt"
    CHILDREN_FILE_PATH = f"{outfolder_path}/children.txt"
    OUTPUT_FILE_PATH = f"{outfolder_path}/reduced_nballs.txt"

    if reduce_dimensionality:
        m.main((f"--reduceAndFix --balls {BALLS_FILE_PATH} --children {CHILDREN_FILE_PATH} \
        --output_path {OUTPUT_FILE_PATH}").split())

    CIRCLES_FILE_PATH = OUTPUT_FILE_PATH

    if visualize_nballs:
        m.main(f" --vis --circles {CIRCLES_FILE_PATH}".split())
