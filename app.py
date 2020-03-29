import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, render_template, request
from nltk.corpus import wordnet as wn
import redis
from rq import Queue
from backgroundtask import background_task
import utils.plotly as util
import runner as r

app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

### Queue stuff
r = redis.Redis()
q = Queue(connection=r)



@app.route("/task")
def task():
    if request.args.get("n"):
        job = q.enqueue(background_task, request.args.get("n"))
        return f"Task ({job.id}) added to queue at {job.enqueued_at}"
    return "No value for count provided"



### Queue stuff done

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
    input_words = text.split()
    print(input_words)

    with open("res/sample_input.txt", "w") as file:
        [file.write(word + "\n") for word in input_words]

    r.run("--no_visualize_nballs")

    word_senses = {}
    word_definitions = {}
    for word in input_words:
        word_wn = wn.synsets(word)
        word_senses[word] = [w.name() for w in word_wn]
        word_definitions[word] = [w.definition() for w in word_wn]

    out = {"input_words": input_words, "word_senses": word_senses, "word_definitions": word_definitions,
           "plotly_json": util.plot_balls()}
    out = json.dumps(out)

    return out


if __name__ == '__main__':
    app.run(debug=True)

print(f"haha {app}")
