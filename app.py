import os

import redis
from flask import Flask, render_template, request, jsonify
from rq import Queue

from utils.backgroundtask import background_ball_generation
from utils.plotly import plot_balls, plot_tree_path

app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

### Queue stuff
r = redis.Redis()
q_high = Queue("high", connection=r)    # start with rq worker high
q_low = Queue("low", connection=r)  # start with rq worker low


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/plotly')
def plotly():
    return plot_balls()

@app.route('/tree')
def tree():
    return plot_tree_path()


@app.route('/', methods=['POST'])
def requested_ball_generation():
    input_words = request.form['inputWords'].split()

    job = q_high.enqueue(background_ball_generation, input_words, job_timeout=600)

    response_object = {
        "status": "success",
        "data": {
            "task_id": job.get_id()
        }
    }

    return jsonify(response_object), 202


@app.route('/tasks', methods=['POST'])
def get_status():
    task = q_high.fetch_job(request.form["taskid"])
    queued_job_ids = q_high.job_ids
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
                "queued_job_ids": queued_job_ids
            },
        }
    else:
        response_object = {"status": "error"}
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(debug=True)
