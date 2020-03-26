import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, render_template, request
from nltk.corpus import wordnet as wn

import utils.plotly as util
import runner as r

app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/temp')
def contruction():
    return render_template('construction.html')


@app.route('/plotly')
def plotly():
   return util.plot_balls()


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['name']

    f = open("userOutputFile.txt", "w+")
    f.write(text)
    f.close()

    input_words = text.split()
    print(input_words)

    word_senses = {}
    word_definitions = {}
    for word in input_words:
        word_wn = wn.synsets(word)
        word_senses[word] = [w.name() for w in word_wn]
        word_definitions[word] = [w.definition() for w in word_wn]

    out = {"input_words": input_words, "word_senses": word_senses, "word_definitions": word_definitions}
    out = json.dumps(out)
    print(out)

    # r.run()

    return out


if __name__ == '__main__':
    app.run(debug=True)

print(f"haha {app}")
