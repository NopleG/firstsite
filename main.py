from flask import Flask, render_template, request, redirect, url_for, sessions, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import sqlite3
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://test_flask:lPAQMJRfuL@185.158.113.29:5432/test_flask"
db = SQLAlchemy()
db.init_app(app)




class Data_Base1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    site = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Data_Base1 %r>' % self.id


# with app.app_context():
#     db.create_all()

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form['name']
        sql = text('SELECT name FROM testing')
        result = db.session.execute(sql)
        names = [row[0] for row in result]
        return names


    else:
        return render_template('login.html')



if __name__ == "__main__":
    app.run(debug=True)
