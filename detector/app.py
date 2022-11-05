from flask import Flask, render_template, request, Markup, redirect

app = Flask(__name__)

#render prediction results page
@ app.route('/predictions')
def paperChartPredictions():
    title = 'Paper Chart Detector - Predictions'
    return render_template('results.html', title=title)

# render home page
@ app.route('/')
def home():
    title = 'Paper Chart Detector - Home'
    return render_template('home.html', title=title)

