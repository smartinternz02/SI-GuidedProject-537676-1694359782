from flask import Flask, render_template, request,session, redirect, flash
from datetime import datetime
import urllib.request
import os
from flask import send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key ='a'
def showall():
    sql= "SELECT * from JJ_TABLE"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ",  dictionary["CONTACT"])
        print("The Adress is : ",  dictionary["ADDRESS"])
        print("The Role is : ",  dictionary["ROLE"])
        print("The Department is : ",  dictionary["DEPARTMENT"])
        print("The Password is : ",  dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def getdetails(email,password):
    sql= "select * from JJ_TABLE where email='{}' and password='{}'".format(email,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ", dictionary["CONTACT"])
        print("The Address is : ", dictionary["ADDRESS"])
        print("The Role is : ", dictionary["ROLE"])
        print("The Department is : ", dictionary["DEPARTMENT"])
        print("The Password is : ", dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def create_user(conn,name,email,contact,address,role,department,password):
    sql= "INSERT into JJ_TABLE(NAME,EMAIL,CONTACT,ADDRESS,ROLE,DEPARTMENT,PASSWORD,ID) VALUES('{}','{}','{}','{}','{}','{}','{}',NEXT VALUE FOR USER_SEQ)".format(name,email,contact,address,role,department,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))

def add_course(conn,course_nm):
    sql = "INSERT INTO COURSES(COURSE_ID, COURSE_NM, FACULTY_ID, CREATE_DT, CREATE_BY) VALUES(NEXT VALUE FOR COURSE_ID_SEQ, '{}', PREVIOUS VALUE FOR USER_SEQ, CURRENT DATE, 'SYS')".format(course_nm)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))    

def add_assignment(conn, assignment_name, course_id):
    assignment_dt = str(datetime.now())
    due_dt = assignment_dt
    sql = "INSERT INTO ASSIGNMENT(ASSIGNMENT_ID, ASSIGNMENT_NM, ASSIGNMENT_DT, DUE_DT, COURSE_ID) VALUES(NEXT VALUE FOR ASSIGNMENT_ID_SEQ, '{}', {}, '{}', {} )".format(assignment_name, assignment_dt, due_dt, course_id)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt)) 
    
def submit_assignment(conn,assignment_id,student_id,submission_dt,filename1):
    sql= "INSERT into ASSIGNMENT_SUBMISSION(SUBMISSION_ID, ASSIGNMENT_ID, STUDENT_ID, SUBMISSION_DT, FILE_NAME) VALUES(NEXT VALUE FOR ASSIGNMENT_SUBMISSION_SEQ,'{}','{}','{}','{}')".format(assignment_id, student_id, submission_dt, filename1)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))

def update_marks(conn, submission_id, marks_obtained):
    evaluated_on = str(datetime.now())
    sql="UPDATE ASSIGNMENT_SUBMISSION SET MARKS_OBTAINED={}, EVALUATED_ON='{}' WHERE SUBMISSION_ID={}".format(marks_obtained, evaluated_on, submission_id)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))

def get_comments():
    sql= "select * from USER_FEEDBACK"
    stmt = ibm_db.exec_immediate(conn, sql)
    comments = ibm_db.fetch_both(stmt)
    while comments != False:
        print("The Name is : ",  comments["ID"])
        print("The E-mail is : ", comments["NAME"])
        print("The Contact is : ", comments["EMAIL"])
        print("The Address is : ", comments["REGISTRATION_NO"])
        print("The Role is : ", comments["FEEDBACK_COMMENTS"])
        comments = ibm_db.fetch_both(stmt)
    return comments

def insert_feedback(conn, email, name, registration_no, feedback_comments):
    sql= "INSERT into USER_FEEDBACK VALUES(NEXT VALUE FOR FEEDBACK_COMMENTS_SEQ,'{}','{}','{}','{}')".format(name, email, registration_no, feedback_comments)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qzw20690;PWD=4QXenxs5r1fHLIN7",'','')
print(conn)
print("connection successful...")

@app.route('/')
def index():
    #return render_template('registration.html')
    return render_template('index.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/feedback', methods=['POST','GET'])
def feedback():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        registration_no = request.form['registrationNumber']
        feedback_comments = request.form['feedback']
        
        insert_feedback(conn, email, name, registration_no, feedback_comments)
        msg = "Feedback submitted successfully."
        return render_template('contactus.html', msg=msg)   
        
@app.route('/fill_registration_form')
def fill_registration_form():
    return render_template('adminregister.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        contact = request.form['mobile']
        address = request.form['address']
        role = request.form['role']
        if role =="0":
            role = "Faculty"
        elif role == "1":
            role = "Student"
        else:
            role = "New Admin"
        department = request.form['department']
        password = request.form['pwd']
        
        create_user(conn,name,email,contact,address,role,department,password)
        #add_faculty(conn,name, email)
        add_course(conn,department)
            
        return render_template('login.html')
        

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pwd']
        sql= "select * from JJ_TABLE where email='{}' and password='{}'".format(email,password)
        stmt = ibm_db.exec_immediate(conn, sql)
        userdetails = ibm_db.fetch_both(stmt)
        while(userdetails):
            role = ibm_db.result(stmt, "ROLE").strip()
            session['user_email'] =userdetails["EMAIL"]
            session['user_id'] =userdetails["ID"]
            if ((role == "Student")==True):
                loginPage = 'studentprofile.html'
            elif ((role == "Faculty")==True):
                loginPage = 'facultyprofile.html'
            elif ((role == "New Admin")==True):
                loginPage = 'adminprofile.html'
            else:
                msg = "Incorrect Email id or Password"
                return render_template("login.html", msg=msg)
            return render_template(loginPage,name=userdetails["NAME"],email= userdetails["EMAIL"],contact= userdetails["CONTACT"],address=userdetails["ADDRESS"],role=userdetails["ROLE"],department=userdetails["DEPARTMENT"])
    return render_template('login.html')

@app.route('/comments', methods=['GET'])
def comments():
    pageToRender = 'comments.html'
    all_comments = []
    row_cnt = 0
    sql= "select * from USER_FEEDBACK"
    stmt = ibm_db.exec_immediate(conn, sql)
    comments = ibm_db.fetch_assoc(stmt)
    msg="Failed to load"
    while comments != False:
        msg="Loaded successfully"
        all_comments.insert(row_cnt, comments)
        row_cnt=row_cnt+1
        comments = ibm_db.fetch_assoc(stmt)
    return render_template(pageToRender, comments=all_comments, msg=msg)

def get_student_assignment_details(student_id):
    all_assignments = []
    row_cnt = 0
    sql= "SELECT A.ASSIGNMENT_ID, A.ASSIGNMENT_NM, A.ASSIGNMENT_DT, B.SUBMISSION_DT, B.FILE_NAME, B.MARKS_OBTAINED FROM ASSIGNMENT A INNER JOIN COURSES C ON A.COURSE_ID = C.COURSE_ID LEFT OUTER JOIN ASSIGNMENT_SUBMISSION B ON A.ASSIGNMENT_ID = B.ASSIGNMENT_ID INNER JOIN JJ_TABLE U ON U.ID={}".format(student_id)
    stmt = ibm_db.exec_immediate(conn, sql)
    assignments = ibm_db.fetch_assoc(stmt)
    while assignments != False:
        all_assignments.insert(row_cnt, assignments)
        row_cnt=row_cnt+1
        assignments = ibm_db.fetch_assoc(stmt)
    return all_assignments

@app.route('/studentassignment', methods=['GET', 'POST'])
def studentassignment():
    pageToRender = 'studentassignment.html'
    if 'user_id' in session: 
        student_id= session['user_id']
        msg="Failed to load"
        all_assignments = get_student_assignment_details(student_id)
        msg="Loaded successfully"
        return render_template(pageToRender, assignments=all_assignments, msg=msg)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/studentsubmit', methods=['GET', 'POST'])
def studentsubmit():
    pageToRender = 'studentassignmentsubmit.html'
    assignment_id = request.form['ASSIGNMENT_ID']
    student_id = session["user_id"]
    submission_dt = str(datetime.now())
    file = request.files['myfile']
    #if file.filename == '':
    #    flash('No image selected for uploading')
    #    return redirect(request.url)
    #if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    submit_assignment(conn,assignment_id,student_id,submission_dt,filename)
    flash('Image successfully uploaded and displayed below')
    all_assignments = get_student_assignment_details(student_id)
    msg="Loaded successfully"
    #return render_template(pageToRender, assignments=all_assignments, msg=msg)
    return render_template(pageToRender, assignments=all_assignments, filename=filename)
       

@app.route('/facultystulist', methods=['GET'])
def facultystulist():
    pageToRender = 'facultystulist.html'
    student_list = []
    row_cnt = 0
    faculty_id = session["user_id"]
    sql= "SELECT S.NAME, C.COURSE_NM FROM COURSES C, JJ_TABLE F, ASSIGNMENT A, ASSIGNMENT_SUBMISSION B, JJ_TABLE S WHERE C.FACULTY_ID = F.ID AND A.ASSIGNMENT_ID = B.ASSIGNMENT_ID AND A.COURSE_ID = C.COURSE_ID AND B.STUDENT_ID = S.ID AND F.ID={};".format(faculty_id)
    stmt = ibm_db.exec_immediate(conn, sql)
    students = ibm_db.fetch_assoc(stmt)
    msg="Failed to load"
    while students != False:
        msg="Loaded successfully"
        student_list.insert(row_cnt, students)
        row_cnt=row_cnt+1
        students = ibm_db.fetch_assoc(stmt)
    return render_template(pageToRender, student_list=student_list, msg=msg)

@app.route('/facultymarks', methods=['GET'])
def facultymarks():
    pageToRender = 'facultymarks.html'
    student_marks_list = []
    row_cnt = 0
    faculty_id=session["user_id"]
    student_id=3 #session["student_id"]
    sql= "SELECT B.SUBMISSION_ID, A.ASSIGNMENT_ID, A.ASSIGNMENT_NM, S.NAME, A.ASSIGNMENT_DT, B.FILE_NAME, B.SUBMISSION_DT, B.MARKS_OBTAINED FROM ASSIGNMENT A, ASSIGNMENT_SUBMISSION B, COURSES C, JJ_TABLE F, JJ_TABLE S WHERE C.FACULTY_ID = F.ID AND A.ASSIGNMENT_ID = B.ASSIGNMENT_ID AND A.COURSE_ID = C.COURSE_ID AND B.STUDENT_ID = S.ID AND F.ID={} AND S.ID={};".format(faculty_id, student_id)
    stmt = ibm_db.exec_immediate(conn, sql)
    student_marks = ibm_db.fetch_assoc(stmt)
    msg="Failed to load"
    while student_marks != False:
        msg="Loaded successfully"
        student_marks_list.insert(row_cnt, student_marks)
        row_cnt=row_cnt+1
        student_marks = ibm_db.fetch_assoc(stmt)
    return render_template(pageToRender, student_marks_list=student_marks_list, msg=msg)

@app.route('/facultymarksupdate', methods=['POST'])
def facultymarksupdate():
    pageToRender = 'facultymarksupdate.html'
    msg="Loaded successfully"
    submission_id=request.form['SUBMISSION_ID']
    marks_given = request.form['marks_given']
    update_marks(conn, submission_id, marks_given)
    return render_template(pageToRender, msg=msg)

@app.route('/facultyassignment', methods=['GET', 'POST'])
def facultyassignment():
    pageToRender = 'facultyassignment.html'    
    if request.method == "POST":
        assignment_name = request.form['assignment_name']
        #sql= "SELECT F.FACULTY_ID, F.FACULTY_NM, C.COURSE_ID, C.COURSE_NM FROM FACULTY F, COURSES C WHERE F.FACULTY_ID=C.FACULTY_ID AND F.FACULTY_ID=1;".format(faculty_email)
        #stmt = ibm_db.exec_immediate(conn, sql)
        #faculty_course_details = ibm_db.fetch_assoc(stmt)
        #while faculty_course_details != False:
            #session['faculty_id'] =faculty_course_details["FACULTY_ID"]
            #session['faculty_nm'] =faculty_course_details["FACULTY_NM"]
            #session['course_id'] =faculty_course_details["COURSE_ID"]
            #session['course_nm'] =faculty_course_details["COURSE_NM"]
        #faculty_id = session['faculty_id']
        #course_id = session['course_id']
        add_assignment(conn, assignment_name, 1)
    return render_template(pageToRender)

@app.route('/download_file<filename>', methods=['GET', 'POST'])
def download_file():
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'],
                           filename='filename',
                           mimetype='application/pdf')           
                
if __name__ =='__main__':
    app.run( debug = True)
