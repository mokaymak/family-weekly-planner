from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Datenbank-Konfiguration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Datenmodell – jetzt mit 'day'
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    task = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(5), nullable=False)   # Format: HH:MM
    day = db.Column(db.String(10), nullable=False)   # z. B. 'Monday', 'Tuesday'

# Startseite (z. B. alle Einträge anzeigen – optional)
@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.day, Entry.time).all()
    return render_template('index.html', entries=entries)

# Haushaltsseite
@app.route('/householdtasks')
def haushalt():
    entries = Entry.query.order_by(Entry.day, Entry.time).all()
    return render_template('householdtasks.html', entries=entries)

# Termine-Seite
@app.route('/appointments')
def termine():
    return render_template('appointments.html')

# Eintrag hinzufügen
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    task = request.form['task']
    time = request.form['time']
    day = request.form['day']  # neuer Parameter

    new_entry = Entry(name=name, task=task, time=time, day=day)
    db.session.add(new_entry)
    db.session.commit()

    return redirect(url_for('haushalt'))  # besser: direkt zurück zur Haushaltsansicht

# Datenbank beim ersten Start erstellen
if __name__ == '__main__':
    with app.app_context():
        print(">>> create_all() wird ausgeführt")
        db.create_all()
    app.run(debug=True)