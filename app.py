from math import ceil

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = '1e594b441b0f7cd81b01f394d68a5c7c'


class CalendarForm(FlaskForm):
    month = IntegerField('Month', validators=[DataRequired(),
                                              NumberRange(min=1, max=12)])
    year = IntegerField('Year', validators=[DataRequired(),
                                            NumberRange(min=1)])
    submit = SubmitField('Print Calendar')


def is_leap(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    return False


def residue_year(year):
    if is_leap(year):
        return 2
    return 1


def residue_month(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 3
    elif month in [4, 6, 9, 11]:
        return 2
    elif month == 2 and is_leap(year):
        return 1
    return 0


@app.route('/', methods=['GET', 'POST'])
def index():
    title = 'Calendar'
    num_rows = None
    day_of_week = None
    days_in_month = None
    form = CalendarForm()
    if form.validate_on_submit():
        year = form.year.data
        month = form.month.data
        month_names = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
        ]
        month_name = month_names[month - 1]
        title = '%s %d Calendar' % (month_name, year)
        days_in_month = residue_month(year, month) + 28
        total_residue = sum([residue_year(i) for i in range(1, year)]) + \
            sum([residue_month(year, i) for i in range(1, month)])
        day_of_week = total_residue % 7 + 1
        num_rows = ceil((days_in_month + day_of_week - 1) / 7)
    return render_template(
        'index.html',
        title=title,
        form=form,
        num_rows=num_rows,
        day_of_week=day_of_week,
        days_in_month=days_in_month
    )


if __name__ == '__main__':
    app.run(debug=True)
