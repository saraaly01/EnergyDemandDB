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
    return render_template('home.html')
@app.route("/home")
def home():
    return render_template('home.html')
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/EDR")
def EDR():
    items = connect('SELECT * FROM building;')
    return render_template('EDG.html', items=items)


@app.route("/results", methods=['POST'])
def result():
    
    #Obtain the general statistics for a building
    if request.form.get('options') == 'option1':
        rows = connect('SELECT * FROM Building WHERE name = ' +'\'' + request.form.get('building1') + '\';')
        heads = ['Name', 'Property ID', 'Year Built','Primary Use', 'Efficiency Factor', 'Gross Floor Area']
        return render_template('my-result.html', rows=rows, heads=heads)

    #Obtain the energy demanded for a building
    elif request.form.get('options') == 'option2':

        #Get the sum of the usage for meters using electricity (EL) and the sum of the usage for meters using natural gas (NG)
        sumEL = connect('SELECT SUM(usage) FROM meter_entry WHERE start_date >= \'' + request.form.get('start_date') + '\' AND end_date <= \'' + request.form.get('end_date') + '\'AND mName LIKE \'EL%\';')
        sumNG = connect('SELECT SUM(usage) FROM meter_entry WHERE start_date >= \'' + request.form.get('start_date') + '\' AND end_date <= \'' + request.form.get('end_date') + '\'AND mName LIKE \'NG%\';')
        
        #Get the efficiency factor of the building
        eff_F = connect('SELECT eff_factor FROM building WHERE name = \'' + request.form.get('building1') + '\';')

        #Mutilpy the sum of the NG meters by a conversion factor of 29.3 to convert therms to kWh
        #Get the total by adding both sums
        total = float(sumEL[0][0]) * float(eff_F[0][0]) + float(eff_F[0][0]) * (float(sumNG[0][0]) * 29.3)
        heads = ['Usage: kWh']
        return render_template('my-result.html', total=total, heads=heads)

    #Obtain the energy demanded for a building by seasonality
    elif request.form.get('options') == 'option3':
        currYear = request.form.get('years')

        #Get the sum of the summer usage for the meter entries
        sumSummerEL = connect('SELECT SUM(usage) FROM meter_entry WHERE start_date >= \'' + currYear + '-03-01\' AND end_date <= \'' + currYear + '-09-20\'' + 'AND mName LIKE \'EL%\';')
        sumSummerNG = connect('SELECT SUM(usage) FROM meter_entry WHERE start_date >= \'' + currYear + '-03-01\' AND end_date <= \'' + currYear + '-09-20\'' + 'AND mName LIKE \'NG%\';')

        #Get the sum of the winter usage for the meter entries
        sumWinterEL = connect('SELECT SUM(usage) FROM meter_entry WHERE start_date >= \'' + currYear + '-01-01\' AND end_date <= \'' + currYear + '-03-19\' OR start_date>= \'' + currYear + '-09-21\' AND end_date <= \'' + currYear + '-12-31\'' 'AND mName LIKE \'EL%\';')
        sumWinterNG = connect('SELECT SUM(usage) FROM meter_entry WHERE start_date >= \'' + currYear + '-01-01\' AND end_date <= \'' + currYear + '-03-19\' OR start_date>= \'' + currYear + '-09-21\' AND end_date <= \'' + currYear + '-12-31\'' 'AND mName LIKE \'NG%\';')
        
        eff_FS = connect('SELECT eff_factor FROM building WHERE name = \'' + request.form.get('building1') + '\';')
        
        #Total both the Summer and Winter results
        Stotal = float(sumSummerEL[0][0]) * float(eff_FS[0][0]) + float(sumSummerNG[0][0]) * (float(eff_FS[0][0]) * 29.3)
        Wtotal = float(sumWinterEL[0][0]) * float(eff_FS[0][0]) + float(sumWinterNG[0][0]) * (float(eff_FS[0][0]) * 29.3)
        ttl = [Stotal, Wtotal]
        heads= ['Summer Usage: kWh', 'Winter Usage: kWh']
        return render_template('my-result.html', total=ttl, heads=heads)

@app.route('/query-handler', methods=['POST'])
def query_handler():
    rows = connect(request.form['query'])
    return render_template('my-result.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)

