import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    text = db.Column(db.Text)

    def __repr__(self):
        return f'<Call {self.firstname}>'

@app.route('/')
def index():
    calls = Call.query.all()
    return render_template('index.html',calls=calls)
 
@app.route('/<int:call_id>/')
def call(call_id):
    call = Call.query.get_or_404(call_id)
    return render_template('call.html', call=call)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        text = request.form['text']
        call = Call(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          text=text)
        db.session.add(call)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')
    