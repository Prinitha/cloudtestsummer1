from flask import Flask, render_template, flash, request, redirect, url_for
import random
import pypyodbc
import redis
import ast
from time import time
app = Flask(__name__)
connection = pypyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:pxn8557.database.windows.net,1433;Database=DATABASE;Uid=prinitha@pxn8557.database.windows.net,1433;Pwd=chintu@1;")
cursor = connection.cursor()
app.secret_key = "Secret!!!!"
host_name = 'cloudredis.redis.cache.windows.net'
password = 'Nbez9mJY7hUbFWLFAgWp7OJXyku9XIXep7waffZg4z8='
cache = redis.StrictRedis(host=host_name, port=6380, password=password, ssl=True)


@app.route('/')
def hello_world():
    cursor.execute("select count(*) from all_month")
    rows = cursor.fetchall()
    count = rows[0][0]
    return render_template('index.html', count=count)


@app.route('/random_queries')
def random_queries():
    query_limit = request.args['nqueries']
    start_time = time()
    for i in range(0, int(query_limit)):
        cursor.execute('select TOP 1 * from all_month order by rand()')
    end_time = time()
    time_taken = (end_time - start_time) / int(query_limit)
    flash('The Average Time taken to execute the random queries is : ' + "%.4f" % time_taken + " seconds")
    return redirect(url_for('hello_world'))


@app.route('/query_specific')
def query_specific():
    query_limit = request.args['nqueries']
    lower_limit = request.args['low']
    higher_limit = request.args['high']
    start_time = time()
    # magnitude = random.uniform(float(lower_limit), float(higher_limit))
    for i in range(0, int(query_limit)):
        magnitude = random.uniform(float(lower_limit), float(higher_limit))
        if not cache.get(magnitude):
            sql = 'select * from all_month where mag>=? '
            cursor.execute(sql, (magnitude,))
            rows = cursor.fetchall()
            cache.set(magnitude, str(rows))
            flash('In DB Query'+str(magnitude))
        else:
            rows_string = cache.get(magnitude)
            flash('In Cache' + str(magnitude))
    end_time = time()
    time_taken = (end_time - start_time) / int(query_limit)
    flash('The Average Time taken to execute the specific queries is : ' + "%.4f" % time_taken + " seconds")
    # return redirect(url_for('hello_world'))
    return render_template('results.html')


if __name__ == '__main__':
    app.run()
