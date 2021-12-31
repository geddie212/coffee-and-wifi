from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

coffee_rates = ['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕']
wifi_rates = ['💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪']
power_rates = ['🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌']


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=coffee_rates)
    wifi_rating = SelectField('WiFi Rating', validators=[DataRequired()], choices=wifi_rates)
    power_rating = SelectField('Power Outlet Rating', validators=[DataRequired()], choices=power_rates)
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

# def add_new_cafe(cafe_name, location_URL, opening, closing, coffee_rating, wifi_rating, power_rating ):
#     with open('cafe-data.csv', 'a', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',')
#         writer.writerow(['Cafe Name', 'Location', 'Open', 'Close', 'Coffee', 'Wifi', 'Power'])

def add_new_cafe(*fields):
    cafe_info = []
    for field in fields:
        cafe_info.append(field)
    with open('cafe-data.csv', 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(cafe_info)

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafe
        location_url = form.location
        open_time = form.open_time
        close_time = form.close_time
        coffee_rating = form.coffee_rating
        wifi_rating = form.wifi_rating
        power_rating = form.power_rating
        add_new_cafe(cafe_name.data, location_url.data, open_time.data, close_time.data, coffee_rating.data, wifi_rating.data, power_rating.data)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding='utf-8', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
