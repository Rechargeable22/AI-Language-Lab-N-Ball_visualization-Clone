import os, sys
import utils.google_fetch



word_embedding = "res/glove.6B.50d.txt"
words = "res/sample_input.txt"

utils.google_fetch.fetch_glove()

print(os.getcwd())
os.system(f"python main.py --generate_nballs --input {words} --w2v {word_embedding} --output out/test1")