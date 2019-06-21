import pypyodbc
from flask import Flask, render_template, request
from statistics import mean
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

@app.route('/q5', methods=['GET'])
def q5():
    cursor1 = conn.cursor()

    sql1 = 'select StateName from voting where (TotalPop between 2000 and 8000)'
    cursor1.execute(sql1, )
    rows1 = cursor1.fetchall()
    cursor2 = conn.cursor()
    sql2 = 'select StateName from voting where (TotalPop between 8000 and 40000)'
    cursor2.execute(sql2, )
    rows2 = cursor2.fetchall()
    return render_template("test.html", rows1=rows1, rows2=rows2)


@app.route('/q7', methods=['GET'])
def q7():
    cursor = conn.cursor()
    interval = request.args['interval']
    sql = "select" \
          " case " \
          " when TotalPop >=0 and TotalPop <= 10000 then \'0-10\'" \
          " when TotalPop >=10001  and TotalPop <= 20000    then \'10-20\' " \
          " when TotalPop >= 20001 and TotalPop <= 30000   then \'20-30\' " \
          " when TotalPop >= 30001 and TotalPop <= 40000  then \'30-40\' " \
          " when TotalPop >= 40001 and TotalPop <= 50000  then \'40-50\' " \
          " when TotalPop >= 50001 and TotalPop <= 60000  then \'50-60\' " \
          " when TotalPop >= 60001 and TotalPop <= 70000  then \'60-70\' " \
          " when TotalPop >= 70001 and TotalPop <= 80000  then \'70-80\' "\
          " when TotalPop >= 80001 and TotalPop <= 90000  then \'80-90\' " \
          " when TotalPop >= 90001 and TotalPop <= 100000  then \'90-100\' " \
          " end As 'Range'," \
          "count(*) as Number " \
          "from voting" \
          " group by " \
          "case " \
          " when TotalPop >=0 and TotalPop <= 10000 then \'0-10\'" \
          " when TotalPop >=10001  and TotalPop <= 20000    then \'10-20\' " \
          " when TotalPop >= 20001 and TotalPop <= 30000   then \'20-30\' " \
          " when TotalPop >= 30001 and TotalPop <= 40000  then \'30-40\' " \
          " when TotalPop >= 40001 and TotalPop <= 50000  then \'40-50\' " \
          " when TotalPop >= 50001 and TotalPop <= 60000  then \'50-60\' " \
          " when TotalPop >= 60001 and TotalPop <= 70000  then \'60-70\' " \
          " when TotalPop >= 70001 and TotalPop <= 80000  then \'70-80\' "\
          " when TotalPop >= 80001 and TotalPop <= 90000  then \'80-90\' " \
          " when TotalPop >= 90001 and TotalPop <= 100000  then \'90-100\' " \
          "end;"
    cursor.execute(sql, )
    rows = cursor.fetchall()
    pie_chart = pygal.Pie(height=300)
    pie_chart.title = 'Total states'
    for row in rows:
        pie_chart.add(row[0], row[1])
    pie_chart.render()
    # return render_template('question3.html', chart=pie_chart.render_data_uri())
    return render_template("test.html", chart=pie_chart.render_data_uri())


@app.route('/my_display_range_5', methods=['GET'])
def my_display_range_5():
    # long_value = request.args['long']
    # depth_range1 = request.args['depth_range1']
    # depth_range2 = request.args['depth_range2']
    # start_time = time()
    cursor = conn.cursor()
    # sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
    # sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
    # for r in result:
    # state = r[0]
    #         population_values = []
    #         for year in range(1, len(r)):
    #             string_val = r[year]
    #             print(string_val)
    #             # string_val = string_val.replace(",", "")
    #             # int_val = int(string_val)
    #             population_values.append(string_val)
    #         bar_chart.add(state, population_values)

    sql = 'select AVG(TotalPop), SUM(Voted) from StateVoting'
    # sql1 = 'select TotalPop from StateVoting group by StateName'
    # sql2 = 'select count(VotePop) from StateVoting group by StateName'
    # print(sql)
    cursor.execute(sql, )
    rows = cursor.fetchall()
    # rows = int(rows)
    # mean_rows = mean(rows)

    # print(rows)
    # cache.set(magnitude, str(rows))
    # flash('In DB Query' + str())
    # end_time = time()
    # time_taken = (end_time - start_time)
    # flash('Time taken is : ' + "%.4f" % time_taken + " seconds")
    return render_template("test.html", rows=rows)
    # return redirect(url_for('hello_world'))


@app.route('/my_display_range_6', methods=['GET'])
def my_display_range_6():
    cursor = conn.cursor()

    sql = "select" \
" case " \
		   " when PercentVote >=40 and PercentVote <=45 then \'40-45\'" \
		   " when PercentVote >=45.01  and PercentVote <= 50    then \'45-50\' "\
           " when PercentVote >= 50.01 and PercentVote <= 55   then \'50-55\' "\
           " when PercentVote >= 55.01 and PercentVote <= 60  then \'55-60\' "\
           " when PercentVote >= 60.01 and PercentVote <= 65  then \'60-65\' "\
		   " when PercentVote >= 65.01 and PercentVote <= 70  then \'65-70\' "\
		   " when PercentVote >= 70.01 and PercentVote <= 75  then \'70-75\' "\
" end As 'PercentVote',"\
"count(*) as Number " \
"from StateVoting" \
" group by " \
"case " \
		   " when PercentVote >=40 and PercentVote <=45 then \'40-45\'" \
		   " when PercentVote >=45.01  and PercentVote <= 50    then \'45-50\'"\
           " when PercentVote >= 50.01 and PercentVote <= 55   then \'50-55\' "\
           " when PercentVote >= 55.01 and PercentVote <= 60  then \'55-60\' "\
           " when PercentVote >= 60.01 and PercentVote <= 65  then \'60-65\' "\
		   " when PercentVote >= 65.01 and PercentVote <= 70  then \'65-70\' " \
		   " when PercentVote >= 70.01 and PercentVote <= 75  then \'70-75\' " \
"end;"

    cursor.execute(sql, )
    rows = cursor.fetchall()
    pie_chart = pygal.Pie(height=300)
    pie_chart.title = 'PercentVote'
    for row in rows:
        pie_chart.add(row[0], row[1])
    pie_chart.render()
    # return render_template('question3.html', chart=pie_chart.render_data_uri())
    return render_template("test.html", chart=pie_chart.render_data_uri())



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
    sql = "select TOP 5 place,depth from quake6"
    # print(sql)
    cursor = conn.cursor()
    result = cursor.execute(sql).fetchall()
    population_values = []
    state = []
    # i=0
    for r in result:

        # state.append(str(r[0]))
        population_values.append(r[1])
        # state = r[0]
        # population_values = []
        bar_chart.add(r[0], population_values)
    bar_chart.render()
    return render_template('question1.html', chart=bar_chart.render_data_uri())


@app.route('/question2', )
def question2():
    return render_template('question2.html')


@app.route('/question2_execute', methods=['GET'])
def question2_execute():
    cursor = conn.cursor()
    sql = "select TOP 5 latitude,depth from quake6"
    # print(sql)
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
            # population_val = population_val.replace(",", "")
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
# #
# #
# # from flask import Flask, render_template, flash, request, redirect, url_for
# # import random
# # import pypyodbc
# # import redis
# # import ast
# # from time import time
# # app = Flask(__name__)
# # connection = pypyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:pxn8557.database.windows.net,1433;Database=DATABASE;Uid=prinitha@pxn8557.database.windows.net,1433;Pwd=chintu@1;")
# # cursor = connection.cursor()
# # app.secret_key = "Secret!!!!"
# # host_name = 'cloudredis.redis.cache.windows.net'
# # password = 'Nbez9mJY7hUbFWLFAgWp7OJXyku9XIXep7waffZg4z8='
# # cache = redis.StrictRedis(host=host_name, port=6380, password=password, ssl=True)
# #
# #
# # @app.route('/')
# # def hello_world():
# #     cursor.execute("select count(*) from quake6")
# #     rows = cursor.fetchall()
# #     count = rows[0][0]
# #     return render_template('index.html', count=count)
# #
# # @app.route('/my_display_range_5')
# # def display_range():
# #     long_value = request.args['long']
# #     depth_range1 = request.args['depth_range1']
# #     depth_range2 = request.args['depth_range2']
# #     start_time = time()
# #     # sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
# #     # sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
# #     sql = 'select latitude, longitude, [time], depthError from quake6 where ((longitude > ?) and (depthError between ? and ?)) '
# #     # print(sql)
# #     cursor.execute(sql, (long_value, depth_range1, depth_range2))
# #     rows = cursor.fetchall()
# #     # print(rows)
# #     # cache.set(magnitude, str(rows))
# #     # flash('In DB Query' + str())
# #     end_time = time()
# #     time_taken = (end_time - start_time)
# #     flash('Time taken is : ' + "%.4f" % time_taken + " seconds")
# #     return render_template("testpage.html", rows=rows)
# #     # return redirect(url_for('hello_world'))
# #
# #
# # @app.route('/my_query_specific')
# # def my_query_specific():
# #     no_of_queries = request.args['no_of_queries']
# #     depth_range1 = request.args['depth_range1']
# #     depth_range2 = request.args['depth_range2']
# #     # start_time = time()
# #     # j=0
# #     # magnitude = random.uniform(float(lower_limit), float(higher_limit))
# #     for i in range(0, int(no_of_queries)):
# #
# #         # magnitude = random.uniform(float(depth_range1), float(depth_range2))
# #         # if not cache.get(magnitude):
# #         start_time = time()
# #         sql = 'select TOP 2 depthError from quake6 where (depthError between ? and ?) order by NEWID()'
# #         cursor.execute(sql, (depth_range1, depth_range2))
# #         rows = cursor.fetchall()
# #         # cache.set(magnitude, str(rows))
# #         # flash('In DB Query '+str(rows[0][0]))
# #         # else:
# #         #     rows_string = cache.get(magnitude)
# #         #     # rows = ast.literal_eval(rows_string)
# #         #     flash('In Cache ' + str(magnitude))
# #         end_time = time()
# #         time_taken = (end_time - start_time) / int(no_of_queries)
# #         print("**********", rows)
# #         flash('Depth Error 1: ' + str(rows[0][0]) + ' Depth Error 2: ' + str(rows[1][0]) + '.\n The Average Time taken to execute the specific queries is : ' + "%.4f" % time_taken + " seconds")
# #     return redirect(url_for('hello_world'))
# #
# # # @app.route('/display_range')
# # # def display_range():
# # #     no_queries = request.args['no_queries']
# # #     low_range = request.args['low_range']
# # #     high_range = request.args['high_range']
# # #     start_time = time()
# # #     sql = 'select TOP ' + no_queries + ' mag, latitude, longitude from quake6 where mag between ? and ?'
# # #     print(sql)
# # #     cursor.execute(sql, (low_range, high_range))
# # #     rows = cursor.fetchall()
# # #     print(rows)
# # #     # cache.set(magnitude, str(rows))
# # #     # flash('In DB Query' + str())
# # #     end_time = time()
# # #     time_taken = (end_time - start_time)
# # #     flash('Time taken is : ' + "%.4f" % time_taken + " seconds")
# # #     return render_template("testpage.html", rows=rows)
# # #     # return redirect(url_for('hello_world'))
# #
# # @app.route('/random_queries')
# # def random_queries():
# #     query_limit = request.args['nqueries']
# #     start_time = time()
# #     for i in range(0, int(query_limit)):
# #         cursor.execute('select TOP 1 * from quake6 order by rand()')
# #     end_time = time()
# #     time_taken = (end_time - start_time) / int(query_limit)
# #     flash('The Average Time taken to execute the random queries is : ' + "%.4f" % time_taken + " seconds")
# #     return redirect(url_for('hello_world'))
# #
# #
# # @app.route('/query_specific')
# # def query_specific():
# #     query_limit = request.args['nqueries']
# #     lower_limit = request.args['low']
# #     higher_limit = request.args['high']
# #     start_time = time()
# #     # magnitude = random.uniform(float(lower_limit), float(higher_limit))
# #     for i in range(0, int(query_limit)):
# #         magnitude = random.uniform(float(lower_limit), float(higher_limit))
# #         if not cache.get(magnitude):
# #             sql = 'select * from quake6 where depthError > ? '
# #             cursor.execute(sql, (magnitude,))
# #             rows = cursor.fetchall()
# #             cache.set(magnitude, str(rows))
# #             flash('In DB Query '+str(magnitude))
# #         else:
# #             rows_string = cache.get(magnitude)
# #             # rows = ast.literal_eval(rows_string)
# #             flash('In Cache ' + str(magnitude))
# #     end_time = time()
# #     time_taken = (end_time - start_time) / int(query_limit)
# #     flash('The Average Time taken to execute the specific queries is : ' + "%.4f" % time_taken + " seconds")
# #     # return redirect(url_for('hello_world'))
# #     return render_template('results.html')
# #
# #
# # if __name__ == '__main__':
# #     app.run()



# changes = 0
# # required imports
# from flask import *
# import pandas as pd
# import os
# from os import path, walk
# import json
# import sqlite3 as sql
# import redis
# import time
# import pickle
# import random
#
# # port for server access
# port = 80
# host = '0.0.0.0'
# isRemote = False
# debug = True
#
# radis_hostname = ""
# radis_password = ""
# radis_port = 6379
# radis_ssl = False
#
# project_root = os.path.dirname(__file__)
# template_path = os.path.join(project_root, './templates')
# app = Flask(__name__, template_folder=template_path)
#
# # get service information if on IBM Cloud Platform
# env_json_db = ''
# # if 'WEBSITE_INSTANCE_ID' in os.environ:
# #     isRemote = True
# #     debug = False
# #     radis_hostname = "adbapplication.redis.cache.windows.net"
# #     radis_password = "03QdGeHqNJbvldXvRMilQuWj6Mki+cYHMJ9UBVEVyn1c="
# #     radis_port = "6380"
# #     radis_ssl = True
# # else:
# #     port = 80
# #     host = '127.65.43.21'
# #     radis_hostname = "localhost"
# #     radis_password = ""
# #     radis_port = 6379
# #     radis_ssl = False
#
# r = redis.StrictRedis(host=radis_hostname, port=radis_port, db=0, password=radis_password, ssl=radis_ssl)
#
#
# @app.route('/')
# def home():
#     return render_template('home.html')
#
#
# @app.route('/enternew')
# def upload_csv():
#     return render_template('upload.html')
#
#
# @app.route('/addrec', methods=['POST', 'GET'])
# def addrec():
#     if request.method == 'POST':
#         con = sql.connect("database.db")
#         csv = request.files['myfile']
#         file = pd.read_csv(csv)
#         file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None,
#                     dtype=None)
#         con.close()
#         return render_template("result.html", msg="Record inserted successfully")
#
#
# @app.route('/list')
# def list():
#     cache = "mycache"
#     start_t = time.time()
#     query = "select * from Earthquake"
#     if r.exists(cache):
#         t = "with Cache"
#         rows = pickle.loads(r.get(cache))
#         end_t = time.time() - start_t
#         r.delete(cache)
#     else:
#         t = "without Cache"
#         con = sql.connect("database.db")
#         cur = con.cursor()
#         cur.execute(query)
#         rows = cur.fetchall()
#         con.close()
#         r.set(cache, pickle.dumps(rows))
#         end_t = time.time() - start_t
#
#     return render_template("list.html", rows=rows, e=end_t, t=t)
#
#
# @app.route('/mag_list', methods=['GET', 'POST'])
# def mag_list():
#     res = []
#     cache = "mycache"
#     start_t = time.time()
#     for i in range(10):
#         ran_num = round(random.uniform(-2, 8), 2)
#         if r.exists(cache + str(i)):
#             t = "with"
#             rows = pickle.loads(r.get(cache + str(i)))
#             print(len(rows))
#             if rows != None and len(rows) > 0:
#                 res.append(rows)
#         else:
#             query = "Select place,mag,magType from Earthquake where mag=" + str(ran_num)
#             t = "without"
#             con = sql.connect("database.db")
#             cur = con.cursor()
#             cur.execute(query)
#             rows = cur.fetchall()
#             print(len(rows))
#             if rows != None and len(rows) > 0:
#                 res.append(rows)
#             else:
#                 temp = "No rows where mag = " + str(ran_num)
#                 rows.append(temp)
#                 res.append(rows)
#             r.set(cache + str(i), pickle.dumps(rows))
#             con.close()
#
#     end_t = time.time() - start_t
#     # print (res)
#     return render_template("mag_greater.html", data=res, e=end_t, t=t)
#
#
# @app.route('/quakeRange', methods=['POST'])
# def getPointRange():
#     data_r1 = int(request.form['data_m1'])
#     data_r2 = int(request.form['data_m2'])
#     inc = int(request.form['data_inc'])
#     next = data_r1
#     groups = int((data_r2 - data_r1) / inc)
#     data = []
#     for i in range(groups):
#         print(str(next) + ':' + str(next + inc))
#         g1 = next
#         g2 = next + inc
#         query = "SELECT count(*) FROM Earthquake where mag BETWEEN '" + str(g1) + "' AND '" + str(g2) + "' limit 1"
#         con = sql.connect("database.db")
#         cur = con.cursor()
#         cur.execute(query)
#         mag = cur.fetchall()
#
#         next = (next + inc)
#         data.append([str("Range " + str(g1) + ":" + str(g2)), (mag[0][0])])
#     out = {'out': data}
#
#     return render_template('visual.html', page_data=out)
#
#
# def getFileList():
#     extra_dirs = ['templates']
#     extra_files = extra_dirs[:]
#     for extra_dir in extra_dirs:
#         for dirname, dirs, files in walk(extra_dir):
#             for filename in files:
#                 filename = path.join(dirname, filename)
#                 if path.isfile(filename):
#                     extra_files.append(filename)
#     return extra_files
#
#
# if __name__ == "__main__":
#     extra_files = []
#     if debug:
#         extra_files = getFileList()
#     # app.run(extra_files=extra_files, host='0.0.0.0', port='80', debug=True)
#     app.run()
#
#










