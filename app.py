from flask import Flask, render_template, request
import runner as r

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/temp')
def contruction():
    return render_template('construction.html')

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
