from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    plots = [f for f in os.listdir('static') if f.endswith('.png')]
    return render_template('index.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=True)