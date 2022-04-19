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
    rows = connect('SELECT * FROM Building WHERE name = ' + '\''+ request.form.get('building1') +'\';')
    heads = ['Name','Property ID', 'Year Built','Primary Use','Efficiency Factor','Gross Floor Area']
    return render_template('my-result.html', rows = rows, heads = heads)

@app.route('/query-handler', methods=['POST'])
def query_handler():
    rows = connect(request.form['query'])
    return render_template('my-result.html', rows=rows)

if __name__ == '__main__':
    app.run(debug = True)


