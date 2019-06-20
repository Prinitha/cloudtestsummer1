import pypyodbc
from flask import Flask, render_template, request
import pypyodbc as db
# import redis
import pygal

app = Flask(__name__)
# conn = db.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:cloud3dbserver.database.windows.net,1433;Database=cloud3db;Uid=dbuser@cloud3dbserver;Pwd={insert db password here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
conn = pypyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};Server=tcp:pxn8557.database.windows.net,"
    "1433;Database=DATABASE;Uid=prinitha@pxn8557.database.windows.net,"
    "1433;Pwd=chintu@1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")


# redis_connect_dict = {}
# redis_connect_dict['host'] = 'cloud3redis.redis.cache.windows.net'
# redis_connect_dict['port'] = 6380
# redis_connect_dict['db'] = 0
# redis_connect_dict['password'] = 'insert redis password here'
#
# r = redis.StrictRedis(redis_connect_dict['host'],
#                       redis_connect_dict['port'],
#                       redis_connect_dict['db'],
#                       redis_connect_dict['password'],
#                       ssl=True)
#
# bar_chart = pygal.Bar(width=1000, height=500)
# bar_chart.add('a', [1, 2,3,4,5,6,7,8,9])
# bar_chart.add('b', [1, 3,7,8,9,12,10,1])
# bar_chart.add('c', [1, 3,7,8,9,12,10,1])
# bar_chart.add('d', [1, 2,3,4,5,6,7,8,9])

# line = pygal.Bar(width=1000, height=500)
# line.add('a', [1, 2,3,4,5,6,7,8,9])
# line.add('b', [1, 3,7,8,9,12,10,1])

@app.route('/')
def hello_world():
    return render_template('common.html', )


@app.route('/question1', )
def question1():
    return render_template('question1.html')


# @app.route('/question1_execute', methods=['GET'])
# def question1_execute():
#     bar_chart = pygal.Bar(width=1000, height=500)
#     sql = "select * from quake6 where place like '%Texas%' or place like '%Alaska%' or place like '%CA%'"
#     # print(sql)
#     cursor = conn.cursor()
#     result = cursor.execute(sql).fetchall()
#     # population_values = []
#     for r in result:
#         state = r[0]
#         population_values = []
#         for year in range(1, len(r)):
#             string_val = r[year]
#             print(string_val)
#             # string_val = string_val.replace(",", "")
#             # int_val = int(string_val)
#             population_values.append(string_val)
#         bar_chart.add(state, population_values)
#     return render_template('question1.html', chart=bar_chart.render_data_uri())

@app.route('/question1_execute', methods=['GET'])
def question1_execute():
    bar_chart = pygal.Bar(width=1000, height=500)
    # histo_chart = pygal.Histogram()
    # histo_chart = pygal.Bar(width=1000, height=500)
    sql = "select TOP 5 latitude,depth from quake6 group by latitude, depth"
    # print(sql)
    cursor = conn.cursor()
    result = cursor.execute(sql).fetchall()
    population_values = []
    state = []
    for r in result:
        state.append(str(r[0]))
        population_values.append(r[1])
        # state = r[0]
        # population_values = []
        bar_chart.add(str(state), population_values)
    return render_template('question1.html', chart=bar_chart.render_data_uri())


@app.route('/question2', )
def question2():
    return render_template('question2.html')


@app.route('/question2_execute', methods=['GET'])
def question2_execute():
    cursor = conn.cursor()
    sql = "select * from population where State = 'Alabama' or State = 'Florida'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    xy_chart = pygal.XY(stroke=False, height=300)
    xy_chart.title = 'Correlation'
    for r in result:
        db_years = [None, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
        state = ""
        scatterplot_data = []
        for i in range(1, len(r)):
            state = r[0]
            print(r[0])
            population_val = r[i]
            print(r[i])
            population_val = population_val.replace(",", "")
            int_val = int(population_val)
            tuple = (db_years[i], int_val)
            scatterplot_data.append(tuple)
        xy_chart.add(state, scatterplot_data)
    xy_chart.render()
    return render_template('question2.html', chart=xy_chart.render_data_uri())
    # return render_template('question2.html', result=result, chart=bar_chart.render_data_uri(), line =line.render_data_uri() )


@app.route('/question3', )
def question3():
    return render_template('question3.html')


@app.route('/question3_execute', methods=['GET'])
def question3_execute():
    pie_chart = pygal.Pie(height=300)
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    pie_chart.render()
    return render_template('question3.html', chart=pie_chart.render_data_uri())


@app.route('/question4', )
def question4():
    return render_template('question4.html')


@app.route('/question4_execute', methods=['GET'])
def question4_execute():
    cursor = conn.cursor()
    line_chart = pygal.Line()
    line_chart.title = 'BL (in %)'
    line_chart.x_labels = map(str, range(1970, 2015, 5))
    codes = ["IND", "AFG"]
    for code in codes:
        sql = "select entity, BLPercent from educationshare where Code = " + "'" + code + "'"
        print(sql)
        result = cursor.execute(sql).fetchall()
        print(result)
        bp_values = []
        country = ""
        for r in result:
            country = r[0]
            bp_values.append(r[1])
        line_chart.add(country, bp_values)
    return render_template('question4.html', chart=line_chart.render_data_uri())


@app.route('/question7', )
def question7():
    return render_template('question7.html')


@app.route('/question7_execute', methods=['GET'])
def question7_execute():
    bar_chart = pygal.Bar(width=1000, height=500)
    year = str(request.args.get('year'))
    year = 'y_' + year
    lrange1 = request.args.get('lrange1')
    hrange1 = request.args.get('hrange1')
    lrange2 = request.args.get('lrange2')
    hrange2 = request.args.get('hrange2')
    lrange3 = request.args.get('lrange3')
    hrange3 = request.args.get('hrange3')
    range = [lrange1 + '-' + hrange1, lrange2 + '-' + hrange2, lrange3 + '-' + hrange3]
    print(range)
    cursor = conn.cursor()
    sql = "select count(State) from population where " + year + " between " + "'" + lrange1 + "'" + " and " + "'" + hrange1 + "'"
    sql1 = "select count(State) from population where " + year + " between " + "'" + lrange2 + "'" + " and " + "'" + hrange2 + "'"
    sql2 = "select count(State) from population where " + year + " between " + "'" + lrange3 + "'" + " and " + "'" + hrange3 + "'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    print(result)
    answers = []
    answers.append(result[0][0])
    result = cursor.execute(sql1).fetchall()
    answers.append(result[0][0])
    result = cursor.execute(sql2).fetchall()
    answers.append(result[0][0])
    bar_chart.add(range[0], answers[0])
    bar_chart.add(range[1], answers[1])
    bar_chart.add(range[2], answers[2])
    return render_template('question7.html', chart=bar_chart.render_data_uri())


@app.route('/question9', )
def question9():
    return render_template('question9.html')


@app.route('/question9_execute', methods=['GET'])
def question9_execute():
    code = request.args.get('code')
    lyear = int(request.args.get('lyear'))
    hyear = int(request.args.get('hyear'))
    interval = int(request.args.get('inter'))
    cursor = conn.cursor()
    xy_chart = pygal.XY(stroke=False)
    xy_chart.title = 'BL (in %)'
    years = []
    for i in range(lyear, hyear + interval, interval):
        years.append(i)
    print(years)
    # xy_chart.x_labels = map(str, range(lyear, hyear+interval, interval))
    # codes = ["IND","AFG"]
    # for code in codes:
    sql = "select entity, BLPercent from educationshare where Code = " + "'" + code + "'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    bl_values = []
    country = result[0][0]
    print('country')
    print(country)
    for i in range(len(result)):
        bl_values.append(result[i][1])
    print('bl')
    print(bl_values)
    abc = list(zip(years, bl_values))
    xy_chart.add(country, abc)
    return render_template('question9.html', chart=xy_chart.render_data_uri())


@app.route('/question10', )
def question10():
    return render_template('question10.html')


@app.route('/question10_execute', methods=['GET'])
def question10_execute():
    range = int(request.args.get('range'))
    range = range * 1000000
    bar_chart = pygal.Bar(width=1000, height=500)
    year = str(request.args.get('year'))
    year = 'y_' + year
    lrange1 = 0
    hrange1 = lrange1 + range
    lrange2 = hrange1
    hrange2 = hrange1 + range
    lrange3 = hrange2
    hrange3 = hrange2 + range
    range = [str(lrange1) + '-' + str(hrange1), str(lrange2) + '-' + str(hrange2), str(lrange3) + '-' + str(hrange3)]
    print(range)
    cursor = conn.cursor()
    sql = "select count(State) from population where " + year + " between " + "'" + str(
        lrange1) + "'" + " and " + "'" + str(hrange1) + "'"
    sql1 = "select count(State) from population where " + year + " between " + "'" + str(
        lrange2) + "'" + " and " + "'" + str(hrange2) + "'"
    sql2 = "select count(State) from population where " + year + " between " + "'" + str(
        lrange3) + "'" + " and " + "'" + str(hrange3) + "'"
    print(sql)
    result = cursor.execute(sql).fetchall()
    print(result)
    answers = []
    answers.append(result[0][0])
    result = cursor.execute(sql1).fetchall()
    answers.append(result[0][0])
    result = cursor.execute(sql2).fetchall()
    answers.append(result[0][0])
    bar_chart.add(range[0], answers[0])
    bar_chart.add(range[1], answers[1])
    bar_chart.add(range[2], answers[2])
    return render_template('question10.html', chart=bar_chart.render_data_uri())


if __name__ == '_main_':
    app.run()

#
#
# from flask import Flask, render_template, flash, request, redirect, url_for
# import random
# import pypyodbc
# import redis
# import ast
# from time import time
# app = Flask(__name__)
# connection = pypyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:pxn8557.database.windows.net,1433;Database=DATABASE;Uid=prinitha@pxn8557.database.windows.net,1433;Pwd=chintu@1;")
# cursor = connection.cursor()
# app.secret_key = "Secret!!!!"
# host_name = 'cloudredis.redis.cache.windows.net'
# password = 'Nbez9mJY7hUbFWLFAgWp7OJXyku9XIXep7waffZg4z8='
# cache = redis.StrictRedis(host=host_name, port=6380, password=password, ssl=True)
#
#
# @app.route('/')
# def hello_world():
#     cursor.execute("select count(*) from quake6")
#     rows = cursor.fetchall()
#     count = rows[0][0]
#     return render_template('index.html', count=count)
#
# @app.route('/my_display_range_5')
# def display_range():
#     long_value = request.args['long']
#     depth_range1 = request.args['depth_range1']
#     depth_range2 = request.args['depth_range2']
#     start_time = time()
#     # sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
#     # sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
#     sql = 'select latitude, longitude, [time], depthError from quake6 where ((longitude > ?) and (depthError between ? and ?)) '
#     # print(sql)
#     cursor.execute(sql, (long_value, depth_range1, depth_range2))
#     rows = cursor.fetchall()
#     # print(rows)
#     # cache.set(magnitude, str(rows))
#     # flash('In DB Query' + str())
#     end_time = time()
#     time_taken = (end_time - start_time)
#     flash('Time taken is : ' + "%.4f" % time_taken + " seconds")
#     return render_template("testpage.html", rows=rows)
#     # return redirect(url_for('hello_world'))
#
#
# @app.route('/my_query_specific')
# def my_query_specific():
#     no_of_queries = request.args['no_of_queries']
#     depth_range1 = request.args['depth_range1']
#     depth_range2 = request.args['depth_range2']
#     # start_time = time()
#     # j=0
#     # magnitude = random.uniform(float(lower_limit), float(higher_limit))
#     for i in range(0, int(no_of_queries)):
#
#         # magnitude = random.uniform(float(depth_range1), float(depth_range2))
#         # if not cache.get(magnitude):
#         start_time = time()
#         sql = 'select TOP 2 depthError from quake6 where (depthError between ? and ?) order by NEWID()'
#         cursor.execute(sql, (depth_range1, depth_range2))
#         rows = cursor.fetchall()
#         # cache.set(magnitude, str(rows))
#         # flash('In DB Query '+str(rows[0][0]))
#         # else:
#         #     rows_string = cache.get(magnitude)
#         #     # rows = ast.literal_eval(rows_string)
#         #     flash('In Cache ' + str(magnitude))
#         end_time = time()
#         time_taken = (end_time - start_time) / int(no_of_queries)
#         print("**********", rows)
#         flash('Depth Error 1: ' + str(rows[0][0]) + ' Depth Error 2: ' + str(rows[1][0]) + '.\n The Average Time taken to execute the specific queries is : ' + "%.4f" % time_taken + " seconds")
#     return redirect(url_for('hello_world'))
#
# # @app.route('/display_range')
# # def display_range():
# #     no_queries = request.args['no_queries']
# #     low_range = request.args['low_range']
# #     high_range = request.args['high_range']
# #     start_time = time()
# #     sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
# #     print(sql)
# #     cursor.execute(sql, (low_range, high_range))
# #     rows = cursor.fetchall()
# #     print(rows)
# #     # cache.set(magnitude, str(rows))
# #     # flash('In DB Query' + str())
# #     end_time = time()
# #     time_taken = (end_time - start_time)
# #     flash('Time taken is : ' + "%.4f" % time_taken + " seconds")
# #     return render_template("testpage.html", rows=rows)
# #     # return redirect(url_for('hello_world'))
#
# @app.route('/random_queries')
# def random_queries():
#     query_limit = request.args['nqueries']
#     start_time = time()
#     for i in range(0, int(query_limit)):
#         cursor.execute('select TOP 1 * from quake6 order by rand()')
#     end_time = time()
#     time_taken = (end_time - start_time) / int(query_limit)
#     flash('The Average Time taken to execute the random queries is : ' + "%.4f" % time_taken + " seconds")
#     return redirect(url_for('hello_world'))
#
#
# @app.route('/query_specific')
# def query_specific():
#     query_limit = request.args['nqueries']
#     lower_limit = request.args['low']
#     higher_limit = request.args['high']
#     start_time = time()
#     # magnitude = random.uniform(float(lower_limit), float(higher_limit))
#     for i in range(0, int(query_limit)):
#         magnitude = random.uniform(float(lower_limit), float(higher_limit))
#         if not cache.get(magnitude):
#             sql = 'select * from quake6 where depthError > ? '
#             cursor.execute(sql, (magnitude,))
#             rows = cursor.fetchall()
#             cache.set(magnitude, str(rows))
#             flash('In DB Query '+str(magnitude))
#         else:
#             rows_string = cache.get(magnitude)
#             # rows = ast.literal_eval(rows_string)
#             flash('In Cache ' + str(magnitude))
#     end_time = time()
#     time_taken = (end_time - start_time) / int(query_limit)
#     flash('The Average Time taken to execute the specific queries is : ' + "%.4f" % time_taken + " seconds")
#     # return redirect(url_for('hello_world'))
#     return render_template('results.html')
#
#
# if __name__ == '__main__':
#     app.run()
