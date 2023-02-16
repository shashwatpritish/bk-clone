from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)


class Contact(db.Model):
    name = db.Column(db.String(60), primary_key=False,nullable=False)
    email = db.Column(db.String(130), primary_key=True,nullable=False)
    phone = db.Column(db.Integer, primary_key=True,nullable=False)
    address = db.Column(db.String(120),primary_key=False,nullable=False)
    type = db.Column(db.String(50),primary_key=False,nullable=False)


    def __repr__(self):
        return f"{self.name} - {self.email} - {self.phone} - {self.address} - {self.flavour} -"

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact',methods = ['GET','POST'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        type = request.form['type']
        contact = Contact(name=name,email=email,phone=phone,address=address,type=type)
        db.session.add(contact)
        db.session.commit()
    data  = Contact.query.all()
    return render_template("contact.html", data=data)

if __name__=="__main__":
    app.run(debug=True,host="localhost",port=8000)