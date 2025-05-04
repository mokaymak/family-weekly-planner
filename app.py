from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    task = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(5), nullable=False)   
    day = db.Column(db.String(10), nullable=False)   
    entry_type = db.Column(db.String(15), nullable=False)

@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.day, Entry.time).all()
    return render_template('index.html', entries=entries)

@app.route('/householdtasks')
def haushalt():
    entries = Entry.query.filter_by(entry_type="householdtasks").order_by(Entry.day, Entry.time).all()
    return render_template('householdtasks.html', entries=entries, entry_type="householdtasks")


@app.route('/appointments')
def termine():
    entries = Entry.query.filter_by(entry_type="appointments").order_by(Entry.day, Entry.time).all()
    return render_template('appointments.html', entries=entries, entry_type="appointments")

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    task = request.form['task']
    time = request.form['time']
    day = request.form['day']  
    entry_type = request.form['entry_type']

    new_entry = Entry(name=name, task=task, time=time, day=day, entry_type=entry_type)
    db.session.add(new_entry)
    db.session.commit()

    if entry_type == "appointments":
        return redirect(url_for('termine'))
    else:
        return redirect(url_for('haushalt'))
    
@app.route('/delete-selected', methods=['POST'])
def delete_selected():
    ids = request.form.getlist('delete_ids')
    entry_type = request.form['entry_type']

    if ids:
        for entry_id in ids:
            entry = Entry.query.get(entry_id)
            if entry:
                db.session.delete(entry)
        db.session.commit()

    return redirect(url_for('termine' if entry_type == "appointments" else 'haushalt'))

    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)