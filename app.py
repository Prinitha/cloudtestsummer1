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
    cursor.execute("select count(*) from quake6")
    rows = cursor.fetchall()
    count = rows[0][0]
    return render_template('index.html', count=count)

@app.route('/my_display_range_5')
def display_range():
    long_value = request.args['long']
    depth_range1 = request.args['depth_range1']
    depth_range2 = request.args['depth_range2']
    start_time = time()
    # sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
    # sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
    sql = 'select latitude, longitude, [time], depthError from quake6 where ((longitude > ?) and (depthError between ? and ?)) '
    # print(sql)
    cursor.execute(sql, (long_value, depth_range1, depth_range2))
    rows = cursor.fetchall()
    # print(rows)
    # cache.set(magnitude, str(rows))
    # flash('In DB Query' + str())
    end_time = time()
    time_taken = (end_time - start_time)
    flash('Time taken is : ' + "%.4f" % time_taken + " seconds")
    return render_template("testpage.html", rows=rows)
    # return redirect(url_for('hello_world'))


@app.route('/my_query_specific')
def my_query_specific():
    no_of_queries = request.args['no_of_queries']
    depth_range1 = request.args['depth_range1']
    depth_range2 = request.args['depth_range2']
    # start_time = time()
    # j=0
    # magnitude = random.uniform(float(lower_limit), float(higher_limit))
    for i in range(0, int(no_of_queries)):

        # magnitude = random.uniform(float(depth_range1), float(depth_range2))
        # if not cache.get(magnitude):
        start_time = time()
        sql = 'select TOP 2 depthError from quake6 where (depthError between ? and ?) order by rand()'
        cursor.execute(sql, (depth_range1, depth_range2))
        rows = cursor.fetchall()
        # cache.set(magnitude, str(rows))
        # flash('In DB Query '+str(rows[0][0]))
        # else:
        #     rows_string = cache.get(magnitude)
        #     # rows = ast.literal_eval(rows_string)
        #     flash('In Cache ' + str(magnitude))
        end_time = time()
        time_taken = (end_time - start_time) / int(no_of_queries)
        # flash(rows[j])
        # j = j+1
        flash('The Average Time taken to execute the specific queries is : ' + "%.4f" % time_taken + " seconds")
    return redirect(url_for('hello_world'))
    # return render_template('testpage6.html', rows=rows)

# @app.route('/display_range')
# def display_range():
#     no_queries = request.args['no_queries']
#     low_range = request.args['low_range']
#     high_range = request.args['high_range']
#     start_time = time()
#     sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
#     print(sql)
#     cursor.execute(sql, (low_range, high_range))
#     rows = cursor.fetchall()
#     print(rows)
#     # cache.set(magnitude, str(rows))
#     # flash('In DB Query' + str())
#     end_time = time()
#     time_taken = (end_time - start_time)
#     flash('Time taken is : ' + "%.4f" % time_taken + " seconds")
#     return render_template("testpage.html", rows=rows)
#     # return redirect(url_for('hello_world'))

@app.route('/random_queries')
def random_queries():
    query_limit = request.args['nqueries']
    start_time = time()
    for i in range(0, int(query_limit)):
        cursor.execute('select TOP 1 * from quake6 order by rand()')
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
            sql = 'select * from quake6 where mag>=? '
            cursor.execute(sql, (magnitude,))
            rows = cursor.fetchall()
            cache.set(magnitude, str(rows))
            flash('In DB Query '+str(magnitude))
        else:
            rows_string = cache.get(magnitude)
            # rows = ast.literal_eval(rows_string)
            flash('In Cache ' + str(magnitude))
    end_time = time()
    time_taken = (end_time - start_time) / int(query_limit)
    flash('The Average Time taken to execute the specific queries is : ' + "%.4f" % time_taken + " seconds")
    # return redirect(url_for('hello_world'))
    return render_template('results.html')


if __name__ == '__main__':
    app.run()
