from flask import Flask, render_template, request, redirect, url_for, sessions, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import sqlite3
import os
from config import DB_CONNECTION

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_CONNECTION
db = SQLAlchemy()
db.init_app(app)



class Data_Base1(db.Model):
    __tablename__ = 'testing'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    site = db.Column(db.String, nullable=False)

    def repr(self):
        return '<Data_Base1 %r>' % self.id

class Data_Base2(db.Model):
    __tablename__ = 'testing1'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url1 = db.Column(db.String, nullable=False)
    url2 = db.Column(db.String, nullable=False)
    url3 = db.Column(db.String, nullable=False)
    url4 = db.Column(db.String, nullable=False)

# with app.app_context():
#     db.create_all()

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = f"%{request.form['name']}%"
        result = Data_Base1.query.filter(Data_Base1.name.like(name)).all()

        return render_template('login.html', info=result)


    else:
        return render_template('login.html')


@app.route("/addNote", methods=["GET", "POST"])
def addNote():
    if request.method == "POST":
        name = request.form['name']
        url1 = request.form['url1']
        url2 = request.form['url2']
        url3 = request.form['url3']
        url4 = request.form['url4']
        data = Data_Base2(name=name, url1=url1, url2=url2, url3=url3, url4=url4)
        db.session.add(data)
        db.session.commit()
        return render_template('addNote.html')
    else:
        return render_template('addNote.html')


@app.route("/view")
def view():
    result = Data_Base2.query.all()
    return render_template('view.html', info=result)


@app.route("/editNote/<int:id>/", methods=["GET", "POST"])
def editNote(id):
    if id > 0:
        row = Data_Base2.query.filter(Data_Base2.id == id).first()
        if request.method == 'POST':
            row.name = request.form['name']
            row.url1 = request.form['url1']
            row.url2 = request.form['url2']
            row.url3 = request.form['url3']
            row.url4 = request.form['url4']
            db.session.commit()
            return redirect('addNote.html')
        return render_template('editNote.html', info=row)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)