from flask import Flask, render_template, url_for, flash, request
from forms import InputForm
import pandas as pd
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abcde'

@app.route("/", methods=['GET', 'POST'])
def index():
    form = InputForm()
    # Set selectable options

    conn = sqlite3.connect("boss_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT course_code FROM boss")
    courses = cursor.fetchall()
    form.course_code.choices = [(course[0], course[0]) for course in courses]

    cursor.execute("SELECT DISTINCT term FROM boss")
    terms = cursor.fetchall()
    form.terms.choices = [(term[0], term[0]) for term in terms]

    cursor.execute("SELECT DISTINCT bidding_window FROM boss ORDER BY bidding_window")
    bidding_windows = cursor.fetchall()
    form.bidding_windows.choices = [('', 'Any')] +  [(bid[0], bid[0]) for bid in bidding_windows]

    cursor.execute("SELECT DISTINCT instructor FROM boss ORDER BY instructor")
    professors = cursor.fetchall()
    form.professors.choices = [(prof[0], prof[0]) for prof in professors]

    conn.close()
    # if form.validate_on_submit():
    #     flash("Searched",'success')
    # return render_template('home.html', title='result', form=form)
    result_table = None

    if form.validate_on_submit():
        course_code = form.course_code.data
        term = form.terms.data
        bidding_window = "" 
        
        if form.bidding_windows.data == 'Any' or form.bidding_windows.data == '':
            bidding_window = '%'
        else:
            bidding_window = form.bidding_windows.data

        day = ""
        if form.day.data == 'Any' or form.day.data == '..':
            day = '%'
        else:
            day = form.day.data

        time = ""
        if form.start_times.data == 'Any' or form.start_times.data == '..':
            time = '%'
        else:
            time = form.start_times.data

        professor = ""
        if form.professors.data == 'Any' or form.professors.data == 'None':
            professor = '%'
        else:
            professor = form.professors.data
        
        conn = sqlite3.connect("boss_data.db")
        query = """
            SELECT * FROM boss
            WHERE course_code = ?
              AND term = ?
              AND bidding_window LIKE ?
              AND day LIKE ?
              AND start_time LIKE ?
              AND instructor LIKE ?
              AND median_bid != 0
            ORDER BY 
                bidding_window, 
                CASE day
                    WHEN 'MON' THEN 1
                    WHEN 'TUE' THEN 2
                    WHEN 'WED' THEN 3
                    WHEN 'THU' THEN 4
                    WHEN 'FRI' THEN 5
                END,
                start_time
        """
        df = pd.read_sql_query(query, conn, params=(course_code, term, bidding_window, day, time, professor))
        conn.close()
        if df.empty:
            result_table = "<p><strong>No results found.</strong></p>"
        else:
            df['start_time'] = df['start_time'].str.slice(0, 5)
            df['end_time'] = df['end_time'].str.slice(0, 5)

            # table is too long, dropping unimportant (?) columns
            drop_columns = ['venue','school/department', 'd.i.c.e'] # drop session also? Regular Academic Session
            # df = df[[c for c in df.columns if c not in drop_columns]]
            df = df.drop(columns=drop_columns)

            # shortening the names of some columns
            df = df.rename(columns={
                'term': 'Term',
                'session': 'Session',
                'bidding_window': 'Window',
                'course_code': 'Code',
                'description': 'Desc',
                'section': 'Sect',
                'vacancy': 'Vacancy',
                'opening_vacancy': 'Opening',
                'before_process_vacancy': 'Before',
                'after_process_vacancy': 'After',
                'enrolled_students': 'Enrolled',
                'median_bid': 'Median',
                'min_bid': 'Min',
                'instructor': 'Prof',
                'meet': 'Meet',
                'day': 'Day',
                'start_time': 'Start',
                'end_time': 'End'
            })

            result_table = df.to_html(classes="table table-bordered", index=False)

    return render_template('home.html', title='Result', form=form, result=result_table)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
