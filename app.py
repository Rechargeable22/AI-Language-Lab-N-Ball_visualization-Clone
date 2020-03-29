import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, render_template, request, jsonify
from nltk.corpus import wordnet as wn
import redis
from redis import Connection
from rq import Queue, Worker

from backgroundtask import background_task, background_ball_generation
import utils.plotly as util
import runner as r

app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

### Queue stuff
r = redis.Redis()
q = Queue(connection=r)


# @app.route("/task")
# def task():
#     if request.args.get("n"):
#         job = q.enqueue(background_task, request.args.get("n"))
#         return f"Task ({job.id}) added to queue at {job.enqueued_at}"
#     return "No value for count provided"

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
def form_post():
    r = request
    text = request.form['name']
    input_words = text.split()
    print(input_words)

    job = q.enqueue(background_ball_generation, input_words)

    response_object = {
        "status": "success",
        "data": {
            "task_id": job.get_id()
        }
    }

    return jsonify(response_object), 202


@app.route('/tasks', methods=['POST'])
def get_status():
    r = request
    print("get_status", request.form["taskid"])

    task = q.fetch_job(request.form["taskid"])
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }
    else:
        response_object = {"status": "error"}
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(debug=True)

print(f"haha {app}")
