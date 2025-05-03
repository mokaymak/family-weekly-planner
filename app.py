from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/householdtasks')
def haushalt():
    return render_template('householdtasks.html')

@app.route('/appointments')
def termine():
    return render_template('appointments.html')
