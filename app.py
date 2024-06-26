import os
from datetime import datetime
import sqlite3
from datetime import date
from flask import Flask,request,render_template,jsonify,make_response
import uuid
from flask import session
import secrets


#### Defining Flask App
app = Flask(__name__,static_url_path='/static')

posts = []

 #Generate a secure random key for session management
app.secret_key = secrets.token_hex(16)  # 16 bytes (32 characters) is a good choice

#### check if static folder and database folder exists or not
if not os.path.exists('static'):
    os.makedirs('static')

if not os.path.exists('database'):
    os.makedirs('database')

###### sqlite 3 code #######
    
conn = sqlite3.connect('database/lifecare.db', check_same_thread=False)
c = conn.cursor()


###### appointment bokking ######

c.execute('''CREATE TABLE IF NOT EXISTS doctors(
            first_name text,
            last_name text,
            dob date,
            phone_number integer,
            address integer text,
            doc_id integer text,
            password integer text,
            speciality text,
            status integer
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS patients(
            first_name text,
            last_name text,
            dob date,
            phone_number integer,
            password integer text,
            address integer text,
            status integer
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS superusercreds(
            username integer text,
            password integer text
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS doctorappointmentrequests(
            docid integer text,
            patientname integer text,
            patientnum integer text,
            appointmentdate date
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS doctorappointments(
            docid integer text,
            patientname integer text,
            patientnum integer text,
            appointmentdate date
            )''')

###### disease checker ######

c.execute('''CREATE TABLE IF NOT EXISTS Disease(
            id INTEGER PRIMARY KEY,
            symptoms TEXT ,
            predicted_disease TEXT 
            )''')

# Create posts table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id TEXT PRIMARY KEY,
        title TEXT,
        content TEXT,
        likes INTEGER,
        dislikes INTEGER,
        timestamp TEXT
    )
''')
conn.commit()

# Create comments table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id TEXT PRIMARY KEY,
        post_id TEXT,
        content TEXT,
        FOREIGN KEY (post_id) REFERENCES posts(id)
    )
''')
conn.commit()

###############################
c.execute('SELECT * from superusercreds')
conn.commit()
adminuser = c.fetchall()
if not adminuser:
    c.execute("INSERT INTO superusercreds VALUES ('admin','admin')")
    conn.commit()

# c.execute('SELECT * FROM id_and_password')
# c.execute("INSERT INTO id_and_password VALUES ('{}','{}','{}','{}','{}','{}')".format(ent3.get(), ent4.get(),ent5.get(), ent0.get(),ent1.get(), ent2.get()))
# c1.execute('DELETE FROM count')
# c.execute("UPDATE id_and_password SET user_id=(?) WHERE user_id=(?)",(eee4.get(),c3[0][0]))

###########################
def datetoday():
    today = datetime.now().strftime("%Y-%m-%d")
    return today

def checkonlyalpha(x):
    return x.isalpha()

def checkonlynum(x):
    return x.isdigit()

def checkpass(x):
    f1,f2,f3 = False,False,False
    if len(x)<8:
        return False
    if any(c.isalpha() for c in x):
        f1 = True
    if any(c.isdigit() for c in x):
        f2 = True
    if any(c in x for c in ['@','$','!']):
        f3 = True

    return f1 and f2 and f3

def checkphnlen(x):
    return len(x)==10

def retalldocsandapps():
    c.execute(f"SELECT * FROM doctorappointments")
    conn.commit()
    docsandapps = c.fetchall()
    l = len(docsandapps)
    return docsandapps,l

def retdocappointmentsfor(patnum):
    c.execute(f"SELECT * FROM doctorappointments WHERE patientnum='{patnum}'")
    conn.commit()
    docsandapps = c.fetchall()
    l = len(docsandapps)
    return docsandapps, l

def getpatdetails(phn):
    c.execute(f"SELECT * FROM patients")
    conn.commit()
    patients = c.fetchall()
    for i in patients:
        if str(i[3])==str(phn):
            return i

def getdocdetails(docid):
    c.execute(f"SELECT * FROM doctors")
    conn.commit()
    doctors = c.fetchall()
    for i in doctors:
        if str(i[5])==str(docid):
            return i


def retdocsandapps(docid):
    c.execute(f"SELECT * FROM doctorappointments")
    conn.commit()
    docsandapps = c.fetchall()
    docsandapps2 = []
    for i in docsandapps:
        if str(i[0])==str(docid):
            docsandapps2.append(i)
    l = len(docsandapps2)
    return docsandapps2,l

def retapprequests(docid):
    c.execute(f"SELECT * FROM doctorappointmentrequests")
    conn.commit()
    appreq = c.fetchall()
    appreq2 = []
    for i in appreq:
        if str(i[0])==str(docid):
            appreq2.append(i)
    l = len(appreq2)
    return appreq,l

def ret_patient_reg_requests():
    c.execute('SELECT * FROM patients')
    conn.commit()
    data = c.fetchall()
    patient_reg_requests = []
    for d in data:
        if str(d[-1])=='0':
            patient_reg_requests.append(d)
    return patient_reg_requests

def ret_doctor_reg_requests():
    c.execute('SELECT * FROM doctors')
    conn.commit()
    data = c.fetchall()
    doctor_reg_requests = []
    for d in data:
        if str(d[-1])=='0':
            doctor_reg_requests.append(d)
    return doctor_reg_requests

def ret_registered_patients():
    c.execute('SELECT * FROM patients')
    conn.commit()
    data = c.fetchall()
    registered_patients = []
    for d in data:
        if str(d[-1])=='1':
            registered_patients.append(d)
    return registered_patients

def ret_registered_doctors():
    c.execute('SELECT * FROM doctors')
    conn.commit()
    data = c.fetchall()
    registered_doctors = []
    for d in data:
        if str(d[-1])=='1':
            registered_doctors.append(d)
    return registered_doctors

def ret_docname_docspec():
    c.execute('SELECT * FROM doctors')
    conn.commit()
    registered_doctors = c.fetchall()
    docname_docid = []
    for i in registered_doctors:
        docname_docid.append(str(i[0])+' '+str(i[1])+'-'+str(i[5])+'-'+str(i[7]))
    l = len(docname_docid)
    return docname_docid,l

def getdocname(docid):
    c.execute('SELECT * FROM doctors')
    conn.commit()
    registered_doctors = c.fetchall()
    for i in registered_doctors:
        if str(i[5])==str(docid):
            return i[0]+'-'+i[1]

def getpatname(patnum):
    c.execute('SELECT * FROM patients')
    conn.commit()
    details = c.fetchall()
    for i in details:
        if str(i[3])==str(patnum):
            return i[0]+' '+i[1]
    else:
        return -1

def get_all_docids():
    c.execute('SELECT * FROM doctors')
    conn.commit()
    registered_doctors = c.fetchall()
    docids = []
    for i in registered_doctors:
        docids.append(str(i[5]))
    return docids


def get_all_patnums():
    c.execute('SELECT * FROM patients')
    conn.commit()
    registered_patients = c.fetchall()
    patnums = []
    for i in registered_patients:
        patnums.append(str(i[3]))
    return patnums


################## ROUTING FUNCTIONS #########################

#### Our main page
@app.route('/')
def home():
    return render_template('home.html') 


@app.route('/patreg')
def patreg():
    return render_template('patientregistration.html') 


@app.route('/docreg')
def docreg():
    return render_template('doctorregistration.html') 


@app.route('/loginpage1')
def loginpage1():
    return render_template('loginpage1.html') 


@app.route('/loginpage2')
def loginpage2():
    return render_template('loginpage2.html') 


@app.route('/loginpage3')
def loginpage3():
    return render_template('loginpage3.html') 


### Functions for adding Patients
@app.route('/addpatient',methods=['POST'])
def addpatient():
    passw = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['dob']
    phn = request.form['phn']
    address = request.form['address']
    print(firstname,lastname,checkonlyalpha(firstname),checkonlyalpha(lastname))

    if (not checkonlyalpha(firstname)) | (not checkonlyalpha(lastname)):
        return render_template('home.html',mess=f'First Name and Last Name can only contain alphabets.')

    if not checkpass(passw):
        return render_template('home.html',mess=f"Password should be of length 8 and should contain alphabets, numbers and special characters ('@','$','!').") 

    if not checkphnlen(phn):
        return render_template('home.html',mess=f"Phone number should be of length 10.") 

    if str(phn) in get_all_patnums():
        return render_template('home.html',mess=f'Patient with mobile number {phn} already exists.') 
    c.execute(f"INSERT INTO patients VALUES ('{firstname}','{lastname}','{dob}','{phn}','{passw}','{address}',0)")
    conn.commit()
    return render_template('home.html',mess=f'Registration Request sent to Super Admin for Patient {firstname}.') 


### Functions for adding Doctors
@app.route('/adddoctor',methods=['GET','POST'])
def adddoctor():
    passw = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['dob']
    phn = request.form['phn']
    address = request.form['address']
    docid = request.form['docid']
    spec = request.form['speciality']
    
    if not checkonlyalpha(firstname) and not checkonlyalpha(lastname):
        return render_template('home.html',mess=f'First Name and Last Name can only contain alphabets.')

    if not checkonlyalpha(spec):
        return render_template('home.html',mess=f'Doctor Speciality can only contain alphabets.')

    if not checkpass(passw):
        return render_template('home.html',mess=f"Password should be of length 8 and should contain alphabets, numbers and special characters ('@','$','!').") 
    
    if not checkphnlen(phn):
        return render_template('home.html',mess=f"Phone number should be of length 10.") 

    if str(docid) in get_all_docids():
        return render_template('home.html',mess=f'Doctor with Doc ID {docid} already exists.') 
    c.execute(f"INSERT INTO doctors VALUES ('{firstname}','{lastname}','{dob}','{phn}','{address}','{docid}','{passw}','{spec}',0)")
    conn.commit()
    return render_template('home.html',mess=f'Registration Request sent to Super Admin for Doctor {firstname}.') 





## Doctor Login Page
@app.route('/doctorlogin',methods=['GET','POST'])
def doctorlogin():
    docid = request.form['docid']
    passw = request.form['pass']
    c.execute('SELECT * FROM doctors')
    conn.commit()
    registerd_doctors = c.fetchall()

    for i in registerd_doctors:
        if str(i[5])==str(docid) and str(i[6])==str(passw):
            appointment_requests_for_this_doctor,l1 = retapprequests(docid)
            fix_appointment_for_this_doctor,l2 = retdocsandapps(docid)
            return render_template('doctorlogin.html',appointment_requests_for_this_doctor=appointment_requests_for_this_doctor,fix_appointment_for_this_doctor=fix_appointment_for_this_doctor,l1=l1,l2=l2,docname=i[0],docid=docid)

    else:
        return render_template('loginpage2.html',err='Please enter correct credentials...')
    

## Admin Login Page
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    username = request.form['username']
    passw = request.form['pass']
    c.execute('SELECT * FROM superusercreds')
    conn.commit()
    superusercreds = c.fetchall()

    for i in superusercreds:
        if str(i[0])==str(username) and str(i[1])==str(passw):
            patient_reg_requests = ret_patient_reg_requests()
            doctor_reg_requests = ret_doctor_reg_requests()
            registered_patients = ret_registered_patients()
            registered_doctors = ret_registered_doctors()
            l1 = len(patient_reg_requests)
            l2 = len(doctor_reg_requests)
            l3 = len(registered_patients)
            l4 = len(registered_doctors)
            return render_template('adminlogin.html',patient_reg_requests=patient_reg_requests,doctor_reg_requests=doctor_reg_requests,registered_patients=registered_patients,registered_doctors=registered_doctors,l1=l1,l2=l2,l3=l3,l4=l4)
    else:
        return render_template('loginpage3.html',err='Please enter correct credentials...')
    

## Delete patient from database    
@app.route('/deletepatient',methods=['GET','POST'])
def deletepatient():
    patnum = request.values['patnum']
    c.execute(f"DELETE FROM patients WHERE phone_number='{str(patnum)}' ")
    conn.commit()
    patient_reg_requests = ret_patient_reg_requests()
    doctor_reg_requests = ret_doctor_reg_requests()
    registered_patients = ret_registered_patients()
    registered_doctors = ret_registered_doctors()
    l1 = len(patient_reg_requests)
    l2 = len(doctor_reg_requests)
    l3 = len(registered_patients)
    l4 = len(registered_doctors)
    return render_template('adminlogin.html',patient_reg_requests=patient_reg_requests,doctor_reg_requests=doctor_reg_requests,registered_patients=registered_patients,registered_doctors=registered_doctors,l1=l1,l2=l2,l3=l3,l4=l4)
    

## Delete doctor from database
@app.route('/deletedoctor',methods=['GET','POST'])
def deletedoctor():
    docid = request.values['docid']
    c.execute(f"DELETE FROM doctors WHERE doc_id='{str(docid)}' ")
    conn.commit()
    patient_reg_requests = ret_patient_reg_requests()
    doctor_reg_requests = ret_doctor_reg_requests()
    registered_patients = ret_registered_patients()
    registered_doctors = ret_registered_doctors()
    l1 = len(patient_reg_requests)
    l2 = len(doctor_reg_requests)
    l3 = len(registered_patients)
    l4 = len(registered_doctors)
    return render_template('adminlogin.html',patient_reg_requests=patient_reg_requests,doctor_reg_requests=doctor_reg_requests,registered_patients=registered_patients,registered_doctors=registered_doctors,l1=l1,l2=l2,l3=l3,l4=l4)
   

## Patient Function to make appointment
@app.route('/makeappointment',methods=['GET','POST'])
def makeappointment():
    patnum = request.args['phn']
    appdate = request.form['appdate']
    whichdoctor = request.form['whichdoctor']
    docname = whichdoctor.split('-')[0]
    docid = whichdoctor.split('-')[1]
    patname = getpatname(patnum)
    appdate2 = datetime.strptime(appdate, '%Y-%m-%d').strftime("%Y-%m-%d")
    print(appdate2,datetoday())
    if appdate2>datetoday():
        if patname!=-1:
            c.execute(f"INSERT INTO doctorappointmentrequests VALUES ('{docid}','{patname}','{patnum}','{appdate}')")
            conn.commit()
            docsandapps,l = retalldocsandapps()
            docname_docid,l2 = ret_docname_docspec()
            docnames = []
            for i in docsandapps:
                docnames.append(getdocname(i[0]))
            return render_template('patientlogin.html',mess=f'Appointment Request sent to doctor.',docnames=docnames,docsandapps=docsandapps,docname_docid=docname_docid,l=l,l2=l2,patname=patname) 
        else:
            docsandapps,l = retalldocsandapps()
            docname_docid,l2 = ret_docname_docspec()
            docnames = []
            for i in docsandapps:
                docnames.append(getdocname(i[0]))
            return render_template('patientlogin.html',mess=f'No user with such contact number.',docnames=docnames,docsandapps=docsandapps,docname_docid=docname_docid,l=l,l2=l2,patname=patname) 
    else:
        docsandapps,l = retalldocsandapps()
        docname_docid,l2 = ret_docname_docspec()
        docnames = []
        for i in docsandapps:
            docnames.append(getdocname(i[0]))
        return render_template('patientlogin.html',mess=f'Please select a date after today.',docnames=docnames,docsandapps=docsandapps,docname_docid=docname_docid,l=l,l2=l2,patname=patname) 


## Approve Doctor and add in registered doctors
@app.route('/approvedoctor')
def approvedoctor():
    doctoapprove = request.values['docid']
    c.execute('SELECT * FROM doctors')
    conn.commit()
    doctor_requests = c.fetchall()
    for i in doctor_requests:
        if str(i[5])==str(doctoapprove):
            c.execute(f"UPDATE doctors SET status=1 WHERE doc_id={str(doctoapprove)}")
            conn.commit()
            patient_reg_requests = ret_patient_reg_requests()
            doctor_reg_requests = ret_doctor_reg_requests()
            registered_patients = ret_registered_patients()
            registered_doctors = ret_registered_doctors()
            l1 = len(patient_reg_requests)
            l2 = len(doctor_reg_requests)
            l3 = len(registered_patients)
            l4 = len(registered_doctors)
            return render_template('adminlogin.html',mess=f'Doctor Approved successfully!!!',patient_reg_requests=patient_reg_requests,doctor_reg_requests=doctor_reg_requests,registered_patients=registered_patients,registered_doctors=registered_doctors,l1=l1,l2=l2,l3=l3,l4=l4) 
    else:
        patient_reg_requests = ret_patient_reg_requests()
        doctor_reg_requests = ret_doctor_reg_requests()
        registered_patients = ret_registered_patients()
        registered_doctors = ret_registered_doctors()
        l1 = len(patient_reg_requests)
        l2 = len(doctor_reg_requests)
        l3 = len(registered_patients)
        l4 = len(registered_doctors)
        return render_template('adminlogin.html',mess=f'Doctor Not Approved...',patient_reg_requests=patient_reg_requests,doctor_reg_requests=doctor_reg_requests,registered_patients=registered_patients,registered_doctors=registered_doctors,l1=l1,l2=l2,l3=l3,l4=l4) 


## Approve Patient and add in registered patients
@app.route('/approvepatient')
def approvepatient():
    pattoapprove = request.values['patnum']
    c.execute('SELECT * FROM patients')
    conn.commit()
    patient_requests = c.fetchall()
    for i in patient_requests:
        if str(i[3])==str(pattoapprove):
            c.execute(f"UPDATE patients SET status=1 WHERE phone_number={str(pattoapprove)}")
            conn.commit()
            patient_reg_requests = ret_patient_reg_requests()
            doctor_reg_requests = ret_doctor_reg_requests()
            registered_patients = ret_registered_patients()
            registered_doctors = ret_registered_doctors()
            l1 = len(patient_reg_requests)
            l2 = len(doctor_reg_requests)
            l3 = len(registered_patients)
            l4 = len(registered_doctors)
            return render_template('adminlogin.html',mess=f'Patient Approved successfully!!!',patient_reg_requests=patient_reg_requests,doctor_reg_requests=doctor_reg_requests,registered_patients=registered_patients,registered_doctors=registered_doctors,l1=l1,l2=l2,l3=l3,l4=l4) 

    else:
        patient_reg_requests = ret_patient_reg_requests()
        doctor_reg_requests = ret_doctor_reg_requests()
        registered_patients = ret_registered_patients()
        registered_doctors = ret_registered_doctors()
        l1 = len(patient_reg_requests)
        l2 = len(doctor_reg_requests)
        l3 = len(registered_patients)
        l4 = len(registered_doctors)
        return render_template('adminlogin.html',mess=f'Patient Not Approved...',patient_reg_requests=patient_reg_requests,doctor_reg_requests=doctor_reg_requests,registered_patients=registered_patients,registered_doctors=registered_doctors,l1=l1,l2=l2,l3=l3,l4=l4) 


## Approve an appointment request
@app.route('/doctorapproveappointment')
def doctorapproveappointment():
    docid = request.values['docid']
    patnum = request.values['patnum']
    patname = request.values['patname']
    appdate = request.values['appdate']
    c.execute(f"INSERT INTO doctorappointments VALUES ('{docid}','{patname}','{patnum}','{appdate}')")
    conn.commit()
    c.execute(f"DELETE FROM doctorappointmentrequests WHERE patientnum='{str(patnum)}'")
    conn.commit()
    appointment_requests_for_this_doctor,l1 = retapprequests(docid)
    fix_appointment_for_this_doctor,l2 = retdocsandapps(docid)
    return render_template('doctorlogin.html',appointment_requests_for_this_doctor=appointment_requests_for_this_doctor,fix_appointment_for_this_doctor=fix_appointment_for_this_doctor,l1=l1,l2=l2,docid=docid)


## Delete an appointment request
@app.route('/doctordeleteappointment')
def doctordeleteappointment():
    docid = request.values['docid']
    patnum = request.values['patnum']
    c.execute(f"DELETE FROM doctorappointmentrequests WHERE patientnum='{str(patnum)}'")
    conn.commit()
    appointment_requests_for_this_doctor,l1 = retapprequests(docid)
    fix_appointment_for_this_doctor,l2 = retdocsandapps(docid)
    return render_template('doctorlogin.html',appointment_requests_for_this_doctor=appointment_requests_for_this_doctor,fix_appointment_for_this_doctor=fix_appointment_for_this_doctor,l1=l1,l2=l2,docid=docid)


## Delete a doctor registration request
@app.route('/deletedoctorrequest')
def deletedoctorrequest():
    docid = request.values['docid']
    c.execute(f"DELETE FROM doctors WHERE doc_id='{str(docid)}'")
    conn.commit()
    patient_reg_requests = ret_patient_reg_requests()
    doctor_reg_requests = ret_doctor_reg_requests()
    registered_patients = ret_registered_patients()
    registered_doctors = ret_registered_doctors()
    l1 = len(patient_reg_requests)
    l2 = len(doctor_reg_requests)
    l3 = len(registered_patients)
    l4 = len(registered_doctors)
    return render_template('adminlogin.html',patient_reg_requests=patient_reg_requests,doctor_reg_requests=doctor_reg_requests,registered_patients=registered_patients,registered_doctors=registered_doctors,l1=l1,l2=l2,l3=l3,l4=l4) 


## Delete a patient registration request
@app.route('/deletepatientrequest')
def deletepatientrequest():
    patnum = request.values['patnum']
    c.execute(f"DELETE FROM patients WHERE phone_number='{str(patnum)}'")
    conn.commit()
    patient_reg_requests = ret_patient_reg_requests()
    doctor_reg_requests = ret_doctor_reg_requests()
    registered_patients = ret_registered_patients()
    registered_doctors = ret_registered_doctors()
    l1 = len(patient_reg_requests)
    l2 = len(doctor_reg_requests)
    l3 = len(registered_patients)
    l4 = len(registered_doctors)
    return render_template('adminlogin.html',patient_reg_requests=patient_reg_requests,doctor_reg_requests=doctor_reg_requests,registered_patients=registered_patients,registered_doctors=registered_doctors,l1=l1,l2=l2,l3=l3,l4=l4) 


@app.route('/updatepatient')
def updatepatient():
    phn = request.args['phn']
    fn,ln,dob,phn,passw,add,status = getpatdetails(phn)
    return render_template('updatepatient.html',fn=fn,ln=ln,dob=dob,phn=phn,passw=passw,add=add,status=status) 


@app.route('/updatedoctor')
def updatedoctor():
    docid = request.args['docid']
    fn,ln,dob,phn,add,docid,passw,spec,status = getdocdetails(docid)
    return render_template('updatedoctor.html',fn=fn,ln=ln,dob=dob,phn=phn,passw=passw,add=add,status=status,spec=spec,docid=docid) 

@app.route('/makedoctorupdates',methods=['GET','POST'])
def makedoctorupdates():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['dob']
    phn = request.form['phn']
    address = request.form['address']
    docid = request.args['docid']
    spec = request.form['speciality']
    c.execute("UPDATE doctors SET first_name=(?) WHERE doc_id=(?)",(firstname,docid))
    conn.commit()
    c.execute("UPDATE doctors SET last_name=(?) WHERE doc_id=(?)",(lastname,docid))
    conn.commit()
    c.execute("UPDATE doctors SET dob=(?) WHERE doc_id=(?)",(dob,docid))
    conn.commit()
    c.execute("UPDATE doctors SET phone_number=(?) WHERE doc_id=(?)",(phn,docid))
    conn.commit()
    c.execute("UPDATE doctors SET address=(?) WHERE doc_id=(?)",(address,docid))
    conn.commit()
    c.execute("UPDATE doctors SET speciality=(?) WHERE doc_id=(?)",(spec,docid))
    conn.commit()
    return render_template('home.html',mess='Updations Done Successfully!!!') 

    
@app.route('/makepatientupdates',methods=['GET','POST'])
def makepatientupdates():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    dob = request.form['dob']
    phn = request.args['phn']
    address = request.form['address']
    c.execute("UPDATE patients SET first_name=(?) WHERE phone_number=(?)",(firstname,phn))
    conn.commit()
    c.execute("UPDATE patients SET last_name=(?) WHERE phone_number=(?)",(lastname,phn))
    conn.commit()
    c.execute("UPDATE patients SET dob=(?) WHERE phone_number=(?)",(dob,phn))
    conn.commit()
    c.execute("UPDATE patients SET address=(?) WHERE phone_number=(?)",(address,phn))
    conn.commit()
    return render_template('home.html',mess='Updations Done Successfully!!!') 


############################################## DIsease Checker####################################################

disease_symptoms_mapping = {
    'Common Cold': 'fever, cough, sore_throat',
    'Flu': 'fever, cough, body_ache',
    'COVID-19': 'fever, cough, shortness_of_breath',
    'Migraine': 'headache',
    'Asthma': 'shortness_of_breath, cough',
    'Strep Throat': 'sore_throat, fever',
    'Fibromyalgia': 'fatigue, body_ache',
    'Pneumonia': 'fever,  shortness_of_breath, chest_pain',
    'Urinary Tract Infection': 'burning_sensation_during_urination, frequent_urination, lower_abdominal_pain',
    'Gastroenteritis': 'nausea, vomiting, diarrhea, abdominal_pain',
    'Hypertension': 'headache, dizziness, chest_pain, shortness_of_breath',
    'Diabetes': 'excessive_thirst, frequent_urination, fatigue, unexplained_weight_loss',
    'Influenza (Seasonal Flu)': 'fever, chills, muscle_aches, fatigue',
    'Allergies': 'sneezing, runny_nose, itchy_eyes, congestion',
    'Common Anxiety Disorders': 'excessive_worrying, restlessness, fatigue, difficulty_concentrating',
    'Osteoarthritis': 'joint_pain, stiffness, swelling, reduced_range_of_motion',
    'Depression': 'persistent_sadness, loss_of_interest, fatigue, changes_in_sleep',
    'Seasonal Allergies': 'sneezing, runny_nose, itchy_eyes, congestion',
    'Sinusitis': 'facial_pain, headache, congestion, runny_nose',
    'Bronchitis': 'cough, chest_discomfort, fatigue, shortness_of_breath',
    'Gastroesophageal Reflux Disease (GERD)': 'heartburn, regurgitation, chest_pain, difficulty_swallowing',
    'Migraine': 'severe_headache, nausea, sensitivity_to_light, visual_disturbances',
    'Eczema (Atopic Dermatitis)': 'itchy_skin, redness, rash, dry_skin',
    'Hypothyroidism': 'fatigue, weight_gain, dry_skin, sensitivity_to_cold',
    'Hyperthyroidism': 'weight_loss, rapid_heart_rate, irritability, heat_intolerance',
    'Chronic Obstructive Pulmonary Disease (COPD)': 'shortness_of_breath, chronic_cough, wheezing, chest_tightness',
    # Add more symptoms and diseases as needed
}

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_disease():
    symptoms = request.form.get('symptoms')

    # Get selected checkboxes for common symptoms
    selected_symptoms = request.form.getlist('symptom')

    # Combine entered symptoms and selected symptoms, filtering out empty strings
    all_symptoms = [symptom.strip() for symptom in symptoms.split(',') if symptom] + selected_symptoms

    if not all_symptoms:
        return render_template('results.html', message='Please enter symptoms!!!.')

    # Find the disease with the most similar predefined symptoms
    matching_disease = find_matching_disease(all_symptoms)

    if matching_disease:
    # Save data to the database for the combination of symptoms and its corresponding disease
        symptoms_str = ', '.join(all_symptoms)
        matching_disease_str = matching_disease

        c.execute("INSERT INTO Disease (symptoms, predicted_disease) VALUES (?, ?)", (symptoms_str, matching_disease_str))
        conn.commit()

    # Fetch the newly inserted record
        c.execute("SELECT * FROM Disease ORDER BY id DESC LIMIT 1")
        new_entry = c.fetchone()


        if new_entry:
                return render_template('results.html', result={'predicted_disease': new_entry[2], 'symptoms': new_entry[1]})
        else:
                return render_template('results.html', message='Sorry, the disease for your symptoms is not found.')
    

def find_matching_disease(user_symptoms):
    best_match = None
    best_match_count = 0

    for disease, predefined_symptoms in disease_symptoms_mapping.items():
        predefined_symptoms = [symptom.strip() for symptom in predefined_symptoms.split(',')]
        common_symptoms = set(user_symptoms) & set(predefined_symptoms)
        common_symptoms_count = len(common_symptoms)

        if common_symptoms_count > best_match_count:
            best_match = disease
            best_match_count = common_symptoms_count

    return best_match


###################################################################################################################

@app.route('/patientlogin', methods=['GET', 'POST'])
def patientlogin():
    phn = request.form['phn']
    passw = request.form['pass']
    
    c.execute('SELECT * FROM patients')
    conn.commit()
    registerd_patients = c.fetchall()

    for i in registerd_patients:
        if str(i[3]) == str(phn) and str(i[4]) == str(passw):
            # After successful login
            session['phn'] = phn
            session['user_type'] = 'patient'

            # Retrieve other necessary data
            docsandapps, l = retdocappointmentsfor(str(phn))
            docname_docid, l2 = ret_docname_docspec()
            docnames = []

            for i in docsandapps:
                docnames.append(getdocname(i[0]))

            # Render the template with data
            response = make_response(render_template('patientlogin.html', docsandapps=docsandapps, docnames=docnames,
                                   docname_docid=docname_docid, l=l, l2=l2, patname=i[0], phn=phn))
            response.set_cookie('phn', phn)
            return response
    
    # If credentials are incorrect
    return render_template('loginpage1.html', err='Please enter correct credentials...')

@app.route('/book_appointment',methods=['GET','POST'])
def book_appointment():
    docsandapps, l = retalldocsandapps()
    docname_docid, l2 = ret_docname_docspec()
    registered_doctors = ret_registered_doctors()

    print("Registered Doctors:", registered_doctors)  # Check the content in the console

    if request.method == 'POST':
        patnum = request.form['patnum']
        response = make_response(render_template('book_appointment.html', registered_doctors=registered_doctors, l4=len(registered_doctors)))
        response.set_cookie('patphn', patnum)
        return response
    else:
        response = make_response(render_template('book_appointment.html', registered_doctors=registered_doctors, l4=len(registered_doctors)))
        return response
        
    ## Request appointment page
@app.route('/request_appointment',methods=['GET','POST'])
def request_appointment():
    docdetails = getdocdetails(request.args['docid'])
    return render_template('request_appointment.html', docdetails=docdetails)

## Appointment confirmation page
@app.route('/confirmation',methods=['GET','POST'])
def confirmation():
    appdate = request.form['appDate']
    docid = request.form['docId']
    phn = request.cookies.get('phn')
    print("Patient phone number:", phn)  # Print the patient phone number to the console
    patname = getpatname(phn)
    print("Patient name:", patname)  # Print the patient name to the console
    c.execute(f"INSERT INTO doctorappointmentrequests VALUES ('{docid}','{patname}','{phn}','{appdate}')")
    conn.commit()
    return render_template('confirmation.html')




#############################################Discussion Form###################################################

@app.route('/index_disc', methods=['GET', 'POST'])
def index_disc():
    if request.method == 'POST':
        # Handle the POST request
        data = request.get_json()
        sort_order = data.get('sort_order', 'newest')
        sorted_posts = fetch_posts(order=sort_order)
        return jsonify({'posts': sorted_posts})
    else:
        # Handle the GET request
        return render_template('index_disc.html', posts=fetch_posts())

@app.route('/new_post')
def new_post():
    return render_template('new_post.html')

@app.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    post_id = str(uuid.uuid4())
    timestamp = str(datetime.now())
    
    new_post = {
        'id': post_id,
        'title': data['title'],
        'content': data['content'],
        'likes': 0,
        'dislikes': 0,
        'timestamp': timestamp,
    }
    insert_post(new_post)
    return jsonify({'success': True, 'post_id': post_id, 'timestamp': timestamp})

@app.route('/like_dislike', methods=['POST'])
def like_dislike_post():
    data = request.get_json()
    post_id = data['post_id']
    reaction_type = data['reaction_type']

    post = get_post(post_id)
    if post:
        if reaction_type == 'like':
            post['likes'] += 1
        elif reaction_type == 'dislike':
            post['dislikes'] += 1

        update_post(post)
        updated_post = get_post(post_id)
        return jsonify({'success': True, 'post': updated_post})
    else:
        return jsonify({'success': False, 'message': 'Post not found'})

@app.route('/comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    post_id = data['post_id']
    content = data['content']
    comment_id = str(uuid.uuid4())

    new_comment = {
        'id': comment_id,
        'post_id': post_id,
        'content': content,
    }
    insert_comment(new_comment)
    return jsonify({'success': True, 'comment_id': comment_id, 'replies': fetch_comments(post_id)})

def sort_posts(order):
    # Fetch posts from the database and sort based on the given order
    if order == 'newest':
        return fetch_posts(order=True)
    elif order == 'oldest':
        return fetch_posts(order=False)
    else:
        return fetch_posts()

def fetch_posts(order=None):
    if order is not None:
        # Define the base SQL query
        base_query = 'SELECT * FROM posts ORDER BY timestamp'

        # Append DESC or ASC based on the order parameter
        if order == 'newest':
            query = f'{base_query} DESC'
        elif order == 'oldest':
            query = f'{base_query} ASC'
        else:
            # Default to DESC if the order is not recognized
            query = f'{base_query} DESC'

        c.execute(query)
    else:
        c.execute('SELECT * FROM posts')

    posts = c.fetchall()

    # Ensure that each post tuple has enough elements before accessing them
    formatted_posts = [
        {'id': p[0], 'title': p[1], 'content': p[2], 'likes': p[3], 'dislikes': p[4], 'timestamp': p[5]}
        for p in posts if len(p) >= 6
    ]

    return formatted_posts



def get_post(post_id):
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()
    return {'id': post[0], 'title': post[1], 'content': post[2], 'likes': post[3], 'dislikes': post[4], 'timestamp': post[5]} if post else None

def insert_post(post):
    c.execute('INSERT INTO posts (id, title, content, likes, dislikes, timestamp) VALUES (?, ?, ?, ?, ?, ?)',
               (post['id'], post['title'], post['content'], post['likes'], post['dislikes'], post['timestamp']))
    conn.commit()

def update_post(post):
    c.execute('UPDATE posts SET title=?, content=?, likes=?, dislikes=?, timestamp=? WHERE id=?',
                   (post['title'], post['content'], post['likes'], post['dislikes'], post['timestamp'], post['id']))
    conn.commit()

def fetch_comments(post_id):
    c.execute('SELECT * FROM comments WHERE post_id = ?', (post_id,))
    comments = c.fetchall()
    return [{'id': c[0], 'content': c[2]} for c in comments]

def insert_comment(comment):
    c.execute('INSERT INTO comments VALUES (?, ?, ?)', (comment['id'], comment['post_id'], comment['content']))
    conn.commit()
############################################################################################################
    


#### Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True)