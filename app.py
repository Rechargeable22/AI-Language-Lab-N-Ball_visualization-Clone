import os
import random

import redis
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from rq import Queue

from app_utils.back_ball_generation import background_ball_generation, generate_animation_from_log
from balls_generation.files_utils import read_input_words
from app_utils.web_input_parsing import input_text_to_path
from plotly_visualization.graphs_navigator import plot_animation

app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

### Queue stuff
r = redis.Redis()
q_high = Queue("high", connection=r)  # start with rq worker high
q_low = Queue("low", connection=r)  # start with rq worker low
QUEUE_THRESHOLD = 50  # inputs > QUEUE_THRESHOLD => run on the low priority queue


def ball_generation_response(input_words, f):
    if len(input_words) > QUEUE_THRESHOLD:
        job = q_low.enqueue(f, input_words, job_timeout=60000)
        q_name = "low"
    else:
        job = q_high.enqueue(f, input_words, job_timeout=600)
        q_name = "high"

    response_object = {
        "status": "success",
        "data": {
            "task_id": job.get_id(),
            "queue_priority": q_name
        }
    }
    return response_object


@app.route('/')
def index():
    return render_template('home.html')


# @app.route('/plotly')
# def plotly():
#     animation_graph_plot2()
#     return render_template('plotly.html')

@app.route('/tree')
def tree():
    list = []
    return plot_animation(list)


@app.route('/file', methods=['POST'])
def requested_ball_generation_from_file():
    if "file" in request.files:
        file = request.files["file"]
        fn = secure_filename(file.filename)
        if fn != "":
            if fn.rsplit(".")[1] == "txt":
                random_suffix = str(random.randint(0, 1000000)) + "-"
                file.save(os.path.join("out", random_suffix + fn))
                input_words = []
                with open(os.path.join("out", random_suffix + fn), mode="r", encoding="utf-8") as file:
                    for line in file:
                        line = line.replace("\n", "")
                        input_words.append(line)
                input_words = input_text_to_path(str("".join(input_words)))
                return jsonify(ball_generation_response(input_words, background_ball_generation)), 202
            elif fn.rsplit(".")[1] == "json":
                random_suffix = str(random.randint(0, 1000000)) + "-"
                file.save(os.path.join("out", random_suffix + fn))
                input_words = []
                with open(os.path.join("out", random_suffix + fn), mode="r", encoding="utf-8") as file:
                    input_words = file.read().replace('\n', '')
                return jsonify(ball_generation_response(input_words, generate_animation_from_log)), 202

    return jsonify({"status": "failed"}), 400


@app.route('/', methods=['POST'])
def requested_ball_generation():
    input_words = request.form['inputWords']

    print(input_words)
    input_words = input_text_to_path(input_words)
    print(input_words)

    return jsonify(ball_generation_response(input_words, background_ball_generation)), 202


@app.route('/tasks', methods=['POST'])
def get_status():
    # flash("Requested generation")
    res = request.get_json()
    if res["queue_priority"] == "high":
        task = q_high.fetch_job(res["task_id"])
        queued_job_ids = q_high.job_ids
    elif res["queue_priority"] == "low":
        task = q_low.fetch_job(res["task_id"])
        queued_job_ids = q_low.job_ids
    else:
        raise Exception("Unclear which queue to access.")

    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
                "queued_job_ids": queued_job_ids,
                "queue_priority": res["queue_priority"]
            },
        }
    else:
        response_object = {"status": "error"}
    return jsonify(response_object)


@app.route('/learning', methods=['POST'])
def requested_learning_view():
    # collect parameters needed
    x = 4
    y = 7
    base = "president"

    # randomly select z entites from wordnet that are somewhat related to the base entity


    # generate x random statements involving the base and z entities that are true per definition. Our groundtruth

    # generate y random statements as before. These are not necessarily be true but depend on the groundtruth

    # let user answer whether he thinks each statement is true or false. Show a Venn Diagram for each statement.
    # It might be more useful to highlight the words in question in a diagram of the whole structure.





    pass
















if __name__ == '__main__':
    app.run(debug=True)
