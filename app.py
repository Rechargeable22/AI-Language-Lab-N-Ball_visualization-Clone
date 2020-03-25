import os
import pandas as pandas
import plotly.express as px
from flask import Flask, render_template, request
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
    df = px.data.gapminder()
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55, range_x=[100, 100000], range_y=[25, 90])
    return fig.show()


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']

    f = open("userOutputFile.txt", "w+")
    f.write(text)
    f.close()
    print(text)

    r.run()

    return text


if __name__ == '__main__':
    app.run(debug=True)

print(f"haha {app}")
