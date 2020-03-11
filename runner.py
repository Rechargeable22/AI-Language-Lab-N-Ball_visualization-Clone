import os, sys
import utils.google_fetch

# What part we run
generate_balls = False
reduce_dimensionality = False
visualize_nballs = True

# word_embedding = "res/glove.6B.50d.txt"
word_embedding = "res/glove.txt"
words = "res/sample_input.txt"

utils.google_fetch.fetch_glove()

if generate_balls:
    os.system(f"python main.py --generate_nballs --input {words} --w2v {word_embedding} --output out/test1")

BALLS_FILE_PATH = "out/test1/nballs.txt"
CHILDREN_FILE_PATH = "out/test1/children.txt"
OUTPUT_FILE_PATH = "out/test1/reduced_nballs.txt"

if reduce_dimensionality:
    os.system(f"python main.py --reduceAndFix --balls {BALLS_FILE_PATH} --children {CHILDREN_FILE_PATH} \
    --output_path {OUTPUT_FILE_PATH}")

CIRCLES_FILE_PATH = OUTPUT_FILE_PATH
WORDS_FILE_PATH = None

if visualize_nballs:
    os.system(f"python main.py --vis --circles {CIRCLES_FILE_PATH}")   # --showenWords {WORDS_FILE_PATH}