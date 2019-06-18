from flask import Flask, render_template, flash, request, redirect, url_for
import pypyodbc
from time import time
app = Flask(__name__)
connection = pypyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:pxn8557.database.windows.net,1433;Database=DATABASE;Uid=prinitha@pxn8557.database.windows.net,1433;Pwd=chintu@1;")


@app.route('/')
def hello_world():
    cursor = connection.cursor()
    cursor.execute("select count(*) from all_month")
    rows = cursor.fetchall()
    count = rows[0][0]
    return render_template('index.html', count=count)


@app.route('/random_queries')
def random_queries():
    query_limit = request.args['nqueries']
    start_time = time()
    cursor = connection.cursor()
    for i in range(0, int(query_limit)):
        cursor.execute('select TOP 1 * from all_month order by rand()')
    end_time = time()
    time_taken = (end_time - start_time) / int(query_limit)
    flash('The Average Time taken to execute the random queries is : ' + "%.4f" % time_taken + " seconds")
    return redirect(url_for('hello_world'))


if __name__ == '__main__':
    app.run()
