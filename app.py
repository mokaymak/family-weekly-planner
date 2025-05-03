from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Datenbank-Konfiguration
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Datenmodell – Definition muss vor create_all() stehen
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    task = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(5), nullable=False)   # Format: HH:MM

# Routen und Funktionen bleiben unverändert
@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.time).all()
    return render_template('index.html', entries=entries)

@app.route('/householdtasks')
def haushalt():
    return render_template('householdtasks.html')

@app.route('/appointments')
def termine():
    return render_template('appointments.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    task = request.form['task']
    time = request.form['time']
    
    new_entry = Entry(name=name, task=task, time=time)
    db.session.add(new_entry)
    db.session.commit()
    
    return redirect(url_for('index'))

# Nur beim ersten Start: Datenbank erstellen (nachdem alle Modelle definiert sind)
if __name__ == '__main__':
    with app.app_context():
        print(">>> create_all() wird ausgeführt")
        db.create_all()
    app.run(debug=True)
