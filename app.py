from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/countries')
def countries():
    country_list = [
        "China",
        "Germany",
        "France",
        "USA",
        "UK",
        "Russia",
    ]
    return render_template('country.html', country_list=country_list)


@app.route('/timer')
def timer():
    time = 300
    return render_template('timer.html', time=time)


@app.route('/timer/<int:num>s')
@app.route('/timer/<int:num>')
def customizeTimer(num):
    return render_template('timer.html', time=num)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
