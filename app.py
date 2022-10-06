from flask import Flask, render_template, flash
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from webforms import UserForm


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testingthis.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASS")}@localhost/cv'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

class Applicants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    job = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    first_name = None
    form = UserForm()
    
    if form.validate_on_submit():
        applicant = Applicants.query.filter_by(email=form.email.data).first()
        if applicant is None:
            first_name = form.first_name.data
            last_name = form.last_name.data
            job = form.job.data
            email = form.email.data

            new_applicant = Applicants(first_name=first_name, last_name=last_name, job=job, email=email)

            db.session.add(new_applicant)
            db.session.commit()
            form.first_name.data = ''
            form.last_name.data = ''
            form.job.data = ''
            form.email.data = ''
            flash('User added successfully!')
        
        else:
            form.email.data = ''
            flash("That email is al ready in use!")
    
    our_applicants = Applicants.query.order_by(Applicants.date_posted)

    return render_template('index.html', 
    form=form, 
    our_applicants=our_applicants, 
    first_name=first_name)


if __name__ == "__main__":
    app.run(debug=True)

