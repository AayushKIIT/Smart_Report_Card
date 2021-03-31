""" 
*imports*
"""
from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,inspect
from sqlalchemy.ext.automap import automap_base
import numpy as np
import pandas as pd
import json
""" 
*initial declarations*
 """
app = Flask(__name__, template_folder='Templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
""" 
*Models*
"""
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine,reflect = True)
inspector = inspect(db.engine)

""" 
*Login Page*
"""
#authentication process
def check(id,password):
    personalDetails = Base.classes.personal_details
    students = db.session.query(personalDetails).all()
    present = False
    for s in students:
        if(s.id==id and str(password)=="kiit@1234"):
            present = True
            break
    return present
def get_column_names(table_name):
    columns = []
    inspector = inspect(db.engine)
    for each in inspector.get_columns(table_name):
        columns.append(each['name'])
    return columns

def return_student_details(id):
    personalDetails = Base.classes.personal_details
    students = db.session.query(personalDetails).all()
    for s in students:
        if(s.id ==  id):
            return s
def get_student_attendance(id):
    Attendance = Base.classes.attendance
    students_attendance = db.session.query(Attendance).all()
    for s in students_attendance:
        if(s.id ==  id):
            return s
def get_domain_data(id):
    domain_details = Base.classes.domain_details
    domain_data = db.session.query(domain_details).all()
    for d in domain_data:
        if(d.id == id):
            return d
def get_semester_details(id):
    semester_details = Base.classes.semester_details
    sem_data = db.session.query(semester_details).all()
    for s in sem_data:
        if s.id == id:
            return s
def get_dept_details(id):
    CS = Base.classes.CS
    CS = db.session.query(CS).filter_by()
    EC = Base.classes.EC
    EC = db.session.query(EC).all()
    HS = Base.classes.HS
    HS = db.session.query(HS).all()
    IT = Base.classes.IT
    IT = db.session.query(IT).all()
    MA = Base.classes.MA
    MA = db.session.query(MA).all()
    subjects = [CS,EC,IT,HS,MA]
    objects = []
    for subject in subjects:
        for each in subject:
            if each.id == id:
                objects.append(each)
    return(objects)  

    return (CS,EC,IT,HS,MA)
""" 
!get the rollnumber of the user and display all information via querying the database.
"""
@app.route('/',methods=['GET','POST'])
def index():
    try:
        if request.method == 'POST': 
            roll_id = int(request.form['rollno'])
            password = request.form['password']
            if(check(roll_id,password)==True):
                student = return_student_details(roll_id)
                domain = get_domain_data(roll_id)
                attendance = get_student_attendance(roll_id)
                sem = get_semester_details(roll_id)
                sem_raw = [sem.Sem1,sem.Sem2,sem.Sem3,sem.Sem4,sem.Sem5]
                best_performance = {"CGPA" : max(sem_raw) ,"semester": (sem_raw.index(max(sem_raw)))+1}
                attendance_raw = [attendance.sem1,attendance.sem2,attendance.sem3, attendance.sem4,attendance.sem5]
                most_active = {"semester":(attendance_raw.index(max(attendance_raw))+1),"attendance": max(attendance_raw)}
                data = [domain.CS,domain.EC,domain.HS,domain.IT,domain.MA]
                labels = ["Computer Science","Electronics","Management and Communication","Information Technology","Maths"]
                strong_domain = labels[data.index(max(data))]

                return render_template("dashboard.html",student=student ,domain = domain, attendance= attendance, sem = sem, best_performance = best_performance, most_active = most_active, strong_domain = strong_domain)
            else:
                return render_template("error.html")
        else:
            return render_template('index.html')
    except:
        return render_template("error.html")

@app.route("/dashboard/<int:id>")
def dashboard(id):
    student = return_student_details(id)
    domain = get_domain_data(id)
    attendance = get_student_attendance(id)
    sem = get_semester_details(id)
    sem_raw = [sem.Sem1,sem.Sem2,sem.Sem3,sem.Sem4,sem.Sem5]
    best_performance = {"CGPA" : max(sem_raw) ,"semester": (sem_raw.index(max(sem_raw)))+1}
    attendance_raw = [attendance.sem1,attendance.sem2,attendance.sem3, attendance.sem4,attendance.sem5]
    most_active = {"semester":(attendance_raw.index(max(attendance_raw))+1),"attendance": max(attendance_raw)}
    data = [domain.CS,domain.EC,domain.HS,domain.IT,domain.MA]
    labels = ["Computer Science","Electronics","Management and Communication","Information Technology","Maths"]
    strong_domain = labels[data.index(max(data))]

    return render_template("dashboard.html",student=student ,domain = domain, attendance= attendance, sem = sem, best_performance = best_performance, most_active = most_active, strong_domain = strong_domain)
    


@app.route("/attendance/<int:id>",methods=['GET','POST'])
def attendance(id):
    student = get_student_attendance(id)
    #data for graph
    labels = ["sem1","sem2","sem3","sem4","sem5"]
    data = [student.sem1,student.sem2,student.sem3,student.sem4,student.sem5]
    other_details = {"current_semester":student.sem5,"Most_Active_in_semester":max(data),"attendance_threshold":bool(student.sem5>75)}
    student_details = return_student_details(id)
    return render_template("attendance.html",labels = labels, data = data, other_details = other_details, student = student_details)

""" 
!radar plot (domain analysis)
 """

@app.route("/domain/<int:id>",methods=['GET','POST'])
def domain(id):
    student = return_student_details(id)
    domains = get_domain_data(id)
    data = [domains.CS,domains.EC,domains.HS,domains.IT,domains.MA]
    labels = ["Computer Science","Electronics","Management and Communication","Information Technology","Maths"]
    strong_domain = labels[data.index(max(data))]
    weak_domain = labels[data.index(min(data))]
    return render_template("domain.html",labels = labels,data = data ,student = student,strong_domain = strong_domain, weak_domain = weak_domain)

@app.route("/semester/<int:id>",methods=['GET','POST'])
def semester(id):
    student = return_student_details(id)
    semester = get_semester_details(id)
    data = [semester.Sem1,semester.Sem2,semester.Sem3,semester.Sem4,semester.Sem5]
    labels = ["Sem1","Sem2","Sem3","Sem4","Sem5"]
    data_dict = {}
    best_performance = {"semester":labels[data.index(max(data))],"CGPA":max(data)}
    for d,l in zip(data,labels):
        data_dict[l] = d 
    return render_template("semester_details.html",student = student,semester = semester, data = data , labels = labels, data_dict = data_dict, best_performance=best_performance)

def get_row_data_from_base_classes_query(base_class,base_class_name):
    data = []
    for column in get_column_names(base_class_name):
        data.append(getattr(base_class,column))
    return data[1:]
def get_dict(base_class,base_class_name):
    data = get_row_data_from_base_classes_query(base_class,base_class_name)
    labels = get_column_names(base_class_name)[1:]
    data_dict = {"data":data,"labels":labels}
    return data_dict
def consistency(data,labels):
    good_consistent = []
    bad_consistent = []
    for each in data:
        if (labels[data.index(max(data))]!=labels[data.index(each)] and (float(max(data) - each) <=0.1)):
            good_consistent.append(labels[data.index(each)])
        elif (labels[data.index(min(data))]!=labels[data.index(each)] and (each - float(min(data)) <=0.1)):
            bad_consistent.append(labels[data.index(each)])
    return list(set(good_consistent)),list(set(bad_consistent))

""" 
?write a function to find out the best,second best and worst performance of the user
 """
def calculate_sub_performance(lod,dept_name):
    mx = {}
    mn = {}
    good_consistent = {}
    bad_consistent = {}
    for i,each in enumerate(lod):
        data = each["data"]
        labels = each["labels"]
        mx[dept_name[i]] = labels[data.index(max(data))]
        good_consistent[dept_name[i]],bad_consistent[dept_name[i]] = consistency(data,labels)
        mn[dept_name[i]] = labels[data.index(min(data))]
    return mx,mn,good_consistent,bad_consistent
@app.route("/subject_stats/<int:id>",methods=['GET','POST'])
def subject_stats(id):
    student = return_student_details(id)
    CS,EC,IT,HS,MA = get_dept_details(id)
    CS_dict = get_dict(CS,"CS")
    EC_dict = get_dict(EC,"EC")
    IT_dict = get_dict(IT,"IT")
    HS_dict = get_dict(HS,"HS")
    MA_dict = get_dict(MA,"MA")
    depts = [CS_dict,EC_dict,IT_dict,HS_dict,MA_dict]
    dept_names = ["CS","EC","IT","HS","MA"]
    mx,mn,good_consistent,bad_consistent = calculate_sub_performance(depts,dept_names)


    return render_template("subject_stats.html",student = student,CS = CS, EC = EC, HS = HS , IT = IT ,MA = MA,CS_dict = get_dict(CS,"CS"),EC_dict = get_dict(EC,"EC"),IT_dict = get_dict(IT,"IT"),HS_dict = get_dict(HS,"HS"),MA_dict = get_dict(MA,"MA"), mx=mx ,mn=mn, good_consistent = good_consistent,bad_consistent = bad_consistent)




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)