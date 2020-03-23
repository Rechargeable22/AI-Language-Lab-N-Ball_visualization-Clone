import pandas as pandas
import plotly.express as px
from flask import Flask, render_template, request
import runner as r

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/temp')
def contruction():
    return render_template('construction.html')

@app.route('/plotly')
def plotly():
    df = px.data.gapminder()

    fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
                     size="pop", color="continent",
                     text="country", log_x=True, size_max=60)
    return fig.show()


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']

    f= open("userOutputFile.txt","w+")
    f.write(text)
    f.close()
    print(text)

    r.run()

    return text

if __name__=='__main__':
    app.run(debug=True)


print(f"haha {app}")
