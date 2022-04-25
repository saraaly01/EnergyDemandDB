"""
Template provided by John Degood at: https://github.com/jdegood/flask7dbs
"""


import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgresSQL database server


def connect(query):
    conn = None
    try:
        # read connection parameters
        params = config()
        print('Connecting to the' + params['database'] + "database...")
        conn = psycopg2.connect(**params)
        print('Connected')

        cur = conn.cursor()

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


# app.py
app = Flask(__name__)

@app.route("/")
def form():
    return render_template('hometest.html')
@app.route("/home")
def home():
    return render_template('hometest.html')
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/EDR")
def EDR():
    items = connect('SELECT * FROM building;')
    return render_template('home.html', items=items)


@app.route("/results", methods=['POST'])
def result():
    if request.form.get('options') == 'option1':
        rows = connect('SELECT * FROM Building WHERE name = ' +
                       '\'' + request.form.get('building1') + '\';')
        heads = ['Name', 'Property ID', 'Year Built',
                 'Primary Use', 'Efficiency Factor', 'Gross Floor Area']
        return render_template('my-result.html', rows=rows, heads=heads)
    elif request.form.get('options') == 'option2':
        sum = connect('SELECT SUM(usage) FROM meter_entry WHERE start_date >= \'' + request.form.get(
            'start_date') + '\' AND end_date <= \'' + request.form.get('end_date') + '\';')
        eff_F = connect('SELECT eff_factor FROM building WHERE name = \'' +
                        request.form.get('building1') + '\';')
        total = float(sum[0][0]) * float(eff_F[0][0])
        heads = ['usage']
        return render_template('my-result.html', total=total, heads=heads)
    elif request.form.get('options') == 'option3':
        currYear = request.form.get('years')
        sumSummer = connect('SELECT SUM(usage) FROM meter_entry WHERE start_date >= \'' +
                            currYear + '-03-01\' AND end_date <= \'' + currYear + '-09-20\';')
        sumWinter = connect('SELECT SUM(usage) FROM meter_entry WHERE start_date >= \'' + currYear + '-01-01\' AND end_date <= \'' +
                            currYear + '-03-19\' OR start_date>= \'' + currYear + '-09-21\' AND end_date <= \'' + currYear + '-12-31\';')
        eff_FS = connect(
            'SELECT eff_factor FROM building WHERE name = \'' + request.form.get('building1') + '\';')
        Stotal = float(sumSummer[0][0]) * float(eff_FS[0][0])
        Wtotal = float(sumWinter[0][0]) * float(eff_FS[0][0])
        ttl = [Stotal, Wtotal]
        heads = ['Summer Usage', 'Winter Usage']
		#FIXME: restructure format to not use a list
        return render_template('my-result.html', total=ttl, heads=heads)



@app.route('/query-handler', methods=['POST'])
def query_handler():
    rows = connect(request.form['query'])
    return render_template('my-result.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
