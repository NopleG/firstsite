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


class Listing(db.Model):
    __tablename__ = 'listing'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, db.ForeignKey('goods.url'), nullable=False)
    url1 = db.Column(db.String, db.ForeignKey('goods.url'), nullable=True)
    url2 = db.Column(db.String, db.ForeignKey('goods.url'), nullable=True)
    url3 = db.Column(db.String, db.ForeignKey('goods.url'), nullable=True)
    url4 = db.Column(db.String, db.ForeignKey('goods.url'), nullable=True)

    url_1 = db.relationship("Goods", foreign_keys=url1, lazy='select', backref='listing1')
    url_2 = db.relationship("Goods", foreign_keys=url2, lazy='select', backref='listing2')
    url_3 = db.relationship("Goods", foreign_keys=url3, lazy='select', backref='listing3')
    url_4 = db.relationship("Goods", foreign_keys=url4, lazy='select', backref='listing4')



class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    site = db.Column(db.String, nullable=False)



# with app.app_context():
#     db.create_all()

@app.route("/view")
def view():
    result = Listing.query.all()
    # g = Listing.url_1.name
    return render_template('view.html', info=result, pr=g)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = f"%{request.form['name']}%"
        result = Goods.query.filter(Goods.name.like(name)).all()

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
        data = Listing(name=name, url1=url1, url2=url2, url3=url3, url4=url4)
        db.session.add(data)
        db.session.commit()
        return render_template('addNote.html')
    else:
        return render_template('addNote.html')





@app.route("/editNote/<int:id>/", methods=["GET", "POST"])
def editNote(id):
    if id > 0:
        row = Listing.query.filter(Listing.id == id).first()
        if request.method == 'POST':
            row.name = request.form['name']
            row.url1 = request.form['url1']
            row.url2 = request.form['url2']
            row.url3 = request.form['url3']
            row.url4 = request.form['url4']
            db.session.commit()
            return redirect(url_for('editNote', id=row.id))
        return render_template('editNote.html', info=row)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)