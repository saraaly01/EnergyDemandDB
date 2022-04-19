"""
Template provided by John Degood at: https://github.com/jdegood/flask7dbs
"""


import psycopg2
from config import config
from flask import Flask, render_template, request

#Connect to the PostgresSQL database server
def connect(query):
    conn = None
    try:
        #read connection parameters
        params = config()
        print('Connecting to the' + params['database'] + "database...")
        conn = psycopg2.connect(**params)
        print('Connected')

        cur =conn.cursor()

        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return rows

#app.py
app = Flask(__name__)

@app.route("/")
def form():
    items = connect('SELECT * FROM building;')
    return render_template('home.html',items=items)
@app.route("/results", methods=['POST']) 
def result():
    if request.form['option'] == 1:
        rows = connect('SELECT * FROM Building WHERE name = ' + request.form['building1'] + ';')
    return render_template

if __name__ == '__main__':
    app.run(debug = True)


