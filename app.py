""" 
*imports*
"""
from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import numpy as np
import pandas as pd
import json
""" 
*initial declarations*
 """
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
""" 
*Models*
"""
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine,reflect = True)

#creating models for tables in our database
# Attendance = Base.classes.attendance

# results = db.session.query(Attendance).all()
# for r in results:
#     if(r.id == 1830002):
#         print(r.sem1)
""" 
*Login Page*
"""
def check(id):
    personalDetails = Base.classes.personal_details
    students = db.session.query(personalDetails).all()
    present = False
    for s in students:
        if(s.id==id):
            print()
            present = True
            break
    return present
def return_student_details(id):
    personalDetails = Base.classes.personal_details
    students = db.session.query(personalDetails).all()
    for s in students:
        if(s.id ==  id):
            return s
""" 
!get the rollnumber of the user and display all information via querying the database.
"""
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST': 
        roll_id = int(request.form['rollno'])
        if(check(roll_id)==True):
            student = return_student_details(roll_id)
            return render_template("dashboard.html",student=student)
        else:
           return render_template('error.html')
    else:
        return render_template('index.html')
def get_student_attendance(id):
    Attendance = Base.classes.attendance
    students_attendance = db.session.query(Attendance).all()
    for s in students_attendance:
        if(s.id ==  id):
            return s

@app.route("/attendance/<int:id>",methods=['GET','POST'])
def attendance(id):
    student = get_student_attendance(id)
    #data for graph
    labels = ["sem1","sem2","sem3","sem4","sem5"]
    data = [student.sem1,student.sem2,student.sem3,student.sem4,student.sem5]
    return render_template("attendance.html",labels = labels, data = data)
if __name__ == '__main__':
    app.run(debug=True)