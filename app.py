import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, render_template, request
from nltk.corpus import wordnet as wn

import utils.balls_to_json as util
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
    ball = util.balls_to_object("out/test1/reduced_nballs_after.txt")

    fig = go.Figure()

    # Create scatter trace of text labels
    # fig.add_trace(go.Scatter(
    #     x=[1.5, 3.5],
    #     y=[0.75, 2.5],
    #     text=["Unfilled Circle",
    #           "Filled Circle"],
    #     mode="text",
    # ))

    # Set axes properties
    # fig.update_xaxes(range=[0, 4.5], zeroline=False)
    # fig.update_yaxes(range=[0, 4.5])

    circles = []
    for b in ball:
        circles.append(dict(
            type="circle",
            xref="x",
            yref="y",
            x0=b.vector[0] - b.radius,
            y0=b.vector[1] - b.radius,
            x1=b.vector[0] + b.radius,
            y1=b.vector[1] + b.radius,
            line_color="LightSeaGreen",
        ))

    # Add circles
    fig.update_layout(
        shapes=circles,
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
        ),
        xaxis_showgrid=False,
        yaxis_showgrid=False,

    )

    # Set figure size
    # fig.update_layout(width=800, height=800)

    return fig.show(config={'scrollZoom': True})


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
