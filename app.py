import os
import random

import redis
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from rq import Queue

from web_app.Background_ball_generation import background_ball_generation, generate_animation_from_log
from web_app.web_input_parsing import input_text_to_path


app = Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")

"""Connects webserver to redis queue and sets a threshold value for sorting incoming jobs"""
r = redis.Redis()
q_high = Queue("high", connection=r)  # start with 'rq worker high'
q_low = Queue("low", connection=r)  # start with 'rq worker low'
QUEUE_THRESHOLD = 50  # inputs > QUEUE_THRESHOLD => run on the low priority queue


def ball_generation_response(input_words, f):
    """
    Enqueues the task f in the correct queue. Short tasks in the high-priority queue and long in the low-priority queue.
    :param input_words: User input words from which we generate balls
    :param f: The function that shall be perfomed on the input
    :return: Object containing the task_id that can be queried to check the jobs status.
    """
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


@app.route('/', methods=['POST'])
def requested_ball_generation():
    """
    Called when the user enters words to the webapp's form and then submits it.
    """
    input_words = request.form['inputWords']
    print(input_words)
    input_words = input_text_to_path(input_words)
    print(input_words)

    return jsonify(ball_generation_response(input_words, background_ball_generation)), 202


@app.route('/file', methods=['POST'])
def requested_ball_generation_from_file():
    """
    Startes the ball generation process from an uploaded file. This can either be a sequence of words in which case
    it gets processed like manually entered text, or a JSON file in which it's considered to be a generation log file.
    :return: An error if the background task cant be started.
    """
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


@app.route('/tasks', methods=['POST'])
def get_status():
    """
    Server Interface of the Webeapp that can be queried to check on task process of the ball generation.
    Queue_priority and a task_id are required arguments.
    :return:    An error or an object containing either all the data that is needed to render
                the results of the ball generation or the place of the task in the current queue.
    """
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


if __name__ == '__main__':
    app.run(debug=True)
