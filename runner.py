import os, sys

word_embedding = "res/glove.txt"
words = "res/sample_input.txt"
print(os.getcwd())
os.system(f"python main.py --generate_nballs --input {words} --w2v {word_embedding} --output out/test1")