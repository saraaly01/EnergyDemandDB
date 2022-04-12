#!/usr/bin/python3

import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET','POST','PUT'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug = True)
