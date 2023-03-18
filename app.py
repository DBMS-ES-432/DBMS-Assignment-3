

# app = Flask(__name__)
# #app = Flask(__name__, template_folder='template')

# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/maintenance_portal'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# # @app.route('/logout')
# # def logout():
# #    session.pop('loggedin', None)
# #    session.pop('id', None)
# #    session.pop('username', None)
# #    return redirect(url_for('login'))













from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from mysql.connector import connect
import yaml
import uuid
from authlib.integrations.flask_client import OAuth
import random
import smtplib
from email.message import EmailMessage
app = Flask(__name__)

db=yaml.safe_load(open('db.yaml'))


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'maintenance_portal'
# def get_db():
#     conn = connect(
#         host="localhost",
#         user="root",
#         password="password",
#         database="maintenance_portal"
#     )

#     return conn

name = ''
email_id = ''
OTP = None
to_mail = None
mysql = MySQL(app)
oauth = OAuth(app)
# by soumya
@app.route('/test_guest', methods =['GET', 'POST'])
def test_guest():
	return render_template('test_guest.html')

@app.route('/test_hostel', methods =['GET', 'POST'])
def test_hostel():
	return render_template('test_hostel.html')

@app.route('/test_housing', methods =['GET', 'POST'])
def test_housing():
	return render_template('test_housing.html')

@app.route('/test_specific', methods =['GET', 'POST'])
def test_specific():
	return render_template('test_specific.html')

@app.route('/home', methods =['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/test_guest_fill', methods = ['GET','POST'])
def test_guest_fill():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		number = request.form['number']
		subject = request.form['subject']	
		b_r = request.form['b_r']
		domain = request.form['domain']
		subdomain = request.form['subdomain']
		subdomain1 = request.form['subdomain1']
		floor = request.form['floor']
		comp_id = uuid.uuid1()
		cursor = mysql.connection.cursor()
		cursor.execute('\
		INSERT INTO Complaint\
		(Comp_Id,User_ID,Subject,Domain,Sub_Domain1,Sub_Domain2,Location,Specific_Location,Availability,Complaint_Status,Image,Caption)\
		VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
		(str(comp_id.hex),email,subject,domain,subdomain,subdomain1,'Guest House',b_r,'Always','Pending','NULL','NULL'))
		check=cursor.execute('Select * from Guest_House where Floor = %s and Room_No = %s',(floor,b_r))
		if not check:
			cursor.execute('INSERT INTO Guest_House (Floor,Room_No,Email_Id) VALUES (%s,%s,%s)',(floor,b_r,email))
		mysql.connection.commit()
		return render_template('logout.html')
	return render_template('test_guest.html')

@app.route('/test_hostel_fill', methods = ['GET','POST'])
def test_hostel_fill():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		number = request.form['number']
		subject = request.form['subject']
		hostel = request.form['nh']	
		room = request.form['room']
		availability = request.form['time']
		domain = request.form['domain']
		subdomain = request.form['subdomain']
		subdomain1 = request.form['subdomain1']
		image=['image']
		comp_id = uuid.uuid1()
		cursor = mysql.connection.cursor()
		cursor.execute('\
		INSERT INTO Complaint\
		(Comp_Id,User_ID,Subject,Domain,Sub_Domain1,Sub_Domain2,Location,Specific_Location,Availability,Complaint_Status,Image,Caption)\
		VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
		(str(comp_id.hex),email,subject,domain,subdomain,subdomain1,hostel,room,availability,'Pending',image,'NULL'))
		check = cursor.execute('Select * from Hostel where Hostel_Name = %s and Room_No = %s',(hostel,room))
		if not check:
			cursor.execute('INSERT INTO Hostel (Hostel_Name,Room_No,Student_Email_ID) VALUES\
		 	(%s,%s,%s)', (hostel,room,email))
		mysql.connection.commit()
		cursor.close()
		return render_template('logout.html')
	return render_template('test_hostel.html')

@app.route('/test_housing_fill', methods = ['GET','POST'])
def test_housing_fill():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		number = request.form['number']
		subject = request.form['subject']
		apartment = request.form['apartment']	
		corridor = request.form['corridor']
		block = request.form['Block']
		availability = request.form['availability']
		domain = request.form['domain']
		subdomain = request.form['subdomain']
		subdomain1 = request.form['subdomain1']
		image=['image']
		comp_id = uuid.uuid1()
		cursor = mysql.connection.cursor()
		cursor.execute('\
		INSERT INTO Complaint\
		(Comp_Id,User_ID,Subject,Domain,Sub_Domain1,Sub_Domain2,Location,Specific_Location,Availability,Complaint_Status,Image,Caption)\
		VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
		(str(comp_id.hex),email,subject,domain,subdomain,subdomain1,apartment,corridor,availability,'Pending',image,'NULL'))
		check=cursor.execute('Select * from Housing_Updated where Block_Name = %s and Apartment_No = %s',(block,apartment))
		print(check)
		if not check:
			cursor.execute('INSERT into Housing_Updated (Block_Name,Apartment_No,Email_ID)\
		 	Values (%s,%s,%s)',(block,apartment,email))
		mysql.connection.commit()
		cursor.close()
		return render_template('logout.html')
	return render_template('test_housing.html')

@app.route('/test_specific_fill', methods = ['GET','POST'])
def test_specific_fill():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		number = request.form['number']
		subject = request.form['subject']
		nh = request.form['nh']	
		location = request.form['location']
		availability = request.form['availability']
		domain = request.form['domain']
		subdomain = request.form['subdomain']
		subdomain1 = request.form['subdomain1']
		image=['image']
		comp_id = uuid.uuid1()
		cursor = mysql.connection.cursor()
		cursor.execute('\
		INSERT INTO Complaint\
		(Comp_Id,User_ID,Subject,Domain,Sub_Domain1,Sub_Domain2,Location,Specific_Location,Availability,Complaint_Status,Image,Caption)\
		VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', \
		(str(comp_id.hex),email,subject,domain,subdomain,subdomain1,nh,location,availability,'Pending',image,'NULL'))
		mysql.connection.commit()
		cursor.close()
		return render_template('home.html')
	return render_template('test_specific.html')


@app.route('/filter',methods=['Get','Post'])
def filter():
	if request.method == 'POST':
		filter = request.form['filter']
		cursor = mysql.connection.cursor()
		print(filter)
		if filter == 'Civil':
			cursor.execute('Select * from Complaint where Domain = %s',(filter,))
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
		elif filter == 'Electrical':
			cursor.execute('Select * from Complaint where Domain = %s',(filter,))
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
		elif filter == 'Air-Conditioning':
			cursor.execute('Select * from Complaint where Domain = %s',(filter,))
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
		elif filter == 'Water Cooler':
			cursor.execute('Select * from Complaint where Domain = %s',(filter,))
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
		elif filter == 'All':
			cursor.execute('Select * from Complaint')
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)

@app.route('/', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		username = request.form['Email_id']
		password = request.form['password']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM User WHERE email_id = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			msg = 'Logged in successfully !'
			return render_template('home.html')
		else:
			msg = 'Incorrect username / password !'
	return render_template('index123.html', msg = msg)

@app.route('/forgot_password')
def forgot_password():
	return render_template("forgot_password.html")

@app.route('/verify')
def verify():
	return render_template("verify.html")


def regError(message):
    flash(message)
    return render_template("index123.html",pageType=['register'],flashType="danger")

@app.route('/admin_page')
def admin_page():
	return render_template('Admin_page.html')


@app.route('/admin', methods = ['GET', 'POST'])
def admin():
	if request.method == 'POST':
		username = request.form['ID']
		password = request.form['password']
		print(username,password)
		if username.lower() == 'admin' and password == 'pass':
			cursor = mysql.connection.cursor()
			cursor.execute("SELECT * FROM Complaint")
			data = cursor.fetchall()
			return render_template('Admin_page.html',data=data)
	return render_template('admin_login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST':
		user_details = request.form
		user_type= user_details['User_Type']
		user_id = user_details['User']
		password = user_details['pas1']
		confirm_password = user_details['pas2']
		contact_no = user_details['number']

		
		global name
		global email_id
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM User WHERE email_id = % s', (email_id, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', name):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor.execute('INSERT INTO User(Email_ID,Name,Contact_No,password ) VALUES(%s,%s,%s,%s)', ( email_id,name,contact_no,password, ))
			if user_type == 'Employee':
				cursor.execute('INSERT INTO employee(Employee_ID, Employee_Email_ID) VALUES(%s,%s)', (user_id, email_id))

			else:
				cursor.execute('INSERT INTO Student(Roll_No, Student_Email_ID) VALUES(%s,%s)', (user_id, email_id))
			mysql.connection.commit()
		msg = 'You have successfully registered !'
		cursor.close()
		return redirect('/')
	#elif request.method == 'POST':
	#	msg = 'Please fill out the form !'
	return render_template('register.html',msg=msg)

 
@app.route('/OTP', methods =["GET", "POST"])
def OTP():
	if request.method == "POST":
		user_details = request.form
		global to_mail
		to_mail = user_details['To_mail']
		#print(to_mail)
		cursor = mysql.connection.cursor()
		cursor.execute("select email_id from User where email_id = %s",(to_mail,))
		account = cursor.fetchone()
		for i in account:
			if i==to_mail:
				global OTP
				OTP=random.randrange(2000, 5000, 3)
				mail = EmailMessage()
				mail.set_content("{} is your OTP for Password Reset ".format(OTP))
				mail['Subject'] = 'Password Reset OTP'
				mail['From'] = "patidarritesh@iitgn.ac.in"
				mail['To'] = "{}".format( to_mail )
				server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
				server.login("patidarritesh@iitgn.ac.in", "Patidar@143321")
				server.send_message(mail)
				server.quit()
				return render_template('new_password.html')
	return render_template("reset.html")
	return render_template("table.html")

@app.route('/new_password', methods =["GET", "POST"])
def new_password():
	if request.method == 'POST':
		global OTP
		global to_mail
		password = request.form['pas1']
		confirm = request.form['pas2']
		otp = request.form['OTP']
		print(password,confirm,otp,OTP)
		if password == confirm and int(otp)==OTP:
			cursor = mysql.connection.cursor()
			cursor.execute("Select * from User where email_id = %s",(to_mail,))
			email = cursor.fetchone()
			for i in email:
				print(i,to_mail)
				if i == to_mail:
					cursor.execute("update User Set password = %s where email_id =%s",(password,to_mail,))
					flash('hooray password changed successfully!')
					mysql.connection.commit()
					return render_template('index123.html')
				error = "Account does not exist"
				return render_template('index123.html',error = error)
	error = "Wrong OTP"
	return render_template('forgot_password.html',error = error)

# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route("/index")
# def index():
# 	if 'loggedin' in session:
# 		return render_template("index.html")
# 	return redirect(url_for('login'))


# @app.route("/display")
# def display():
# 	if 'loggedin' in session:
# 		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 		cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
# 		account = cursor.fetchone()
# 		return render_template("display.html", account = account)
# 	return redirect(url_for('login'))

# @app.route("/update", methods =['GET', 'POST'])
# def update():
# 	msg = ''
# 	if 'loggedin' in session:
# 		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
# 			username = request.form['username']
# 			password = request.form['password']
# 			email = request.form['email']
# 			organisation = request.form['organisation']
# 			address = request.form['address']
# 			city = request.form['city']
# 			state = request.form['state']
# 			country = request.form['country']
# 			postalcode = request.form['postalcode']
# 			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# 			cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
# 			account = cursor.fetchone()
# 			if account:
# 				msg = 'Account already exists !'
# 			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
# 				msg = 'Invalid email address !'
# 			elif not re.match(r'[A-Za-z0-9]+', username):
# 				msg = 'name must contain only characters and numbers !'
# 			else:
# 				cursor.execute('UPDATE accounts SET username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
# 				mysql.connection.commit()
# 				msg = 'You have successfully updated !'
# 		elif request.method == 'POST':
# 			msg = 'Please fill out the form !'
# 		return render_template("update.html", msg = msg)
# 	return redirect(url_for('login'))

@app.route('/google',  methods =['GET', 'POST'])
def google():

	# Google Oauth Config
	# Get client_id and client_secret from environment variables
	# For developement purpose you can directly put it
	# here inside double quotes
	GOOGLE_CLIENT_ID = "14105763444-75bvq8dpckghed5kougj1q83538hdn3v.apps.googleusercontent.com"
	GOOGLE_CLIENT_SECRET = "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"
	
	CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
	oauth.register(
		name='google',
		client_id=GOOGLE_CLIENT_ID,
		client_secret=GOOGLE_CLIENT_SECRET,
		server_metadata_url=CONF_URL,
		userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
		client_kwargs={
			'scope': 'openid email profile'
		}
	)
	
	# Redirect to google_auth function
	redirect_uri = url_for('google_auth', _external=True)
	return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/', methods =['GET', 'POST'])
def google_auth():
	token = oauth.google.authorize_access_token()
	#user = oauth.google.parse_id_token(token)
	#print(" Google User ", user)
	global name
	global email_id
	user = oauth.google.userinfo()
	name = user['name']
	email_id = user['email']
	print(user)

	return redirect('/register')


if __name__ == "__main__":
	# app.run(host ="localhost", port = int("5000"))
	app.run(debug=True)





# from flask import Flask, render_template, request, redirect, session, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re
# #from flaskext.mysql import MySQL


# app = Flask(__name__)
# #app = Flask(__name__, template_folder='template')

# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/maintenance_portal'
# #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# app.secret_key = 'your secret key'
 
 
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'maintenance_portal'

# mysql = MySQL(app)

# # def login():
# #     msg = ''
# #     if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:
# #         email_id = request.form['emial_id']
# #         password = request.form['password']
# #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# #         cursor.execute('SELECT * FROM user WHERE email_id = % s AND password = % s', (email_id, password, ))
# #         account = cursor.fetchone()
# #         if account:
# #             session['loggedin'] = True
# #             session['id'] = account['id']
# #             session['username'] = account['username']
# #             msg = 'Logged in successfully !'
# #             return render_template('home.html', msg = msg)
# #         else:
# #             msg = 'Incorrect username / password !'
# #     return render_template('index123.html', msg = msg)
 



# # @app.route('/logout')
# # def logout():
# #    session.pop('loggedin', None)
# #    session.pop('id', None)
# #    session.pop('username', None)
# #    return redirect(url_for('login'))

# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == 'POST' and 'User_id' in request.form and 'Name' in request.form and 'Email_id' in request.form and 'Contact_no' in request.form and 'password' in request.form and 'confirm_password' in request.form:
#         username = request.form['User_id']
#         email_id = request.form['Email_id']
#         name = request.form['Name']
#         contact_no = request.form['Contact_no']

#         password = request.form['password']
        
#         confirm_password = request.form['confirm_password']
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT * FROM user WHERE email_id = % s', (email_id, ))
#         account = cursor.fetchone()
#         if account: 
#             msg = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
#             msg = 'Invalid email address !'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers !'
#         elif password != confirm_password:
#             msg = 'Password does not match !'
#         else:
#             cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s)', (username, email_id,name,contact_no,password, ))
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('index123.html', msg = msg)


 
    
# if __name__ == "__main__":
#     # app.run(host ="localhost", port = int("5000"))
#     app.run(debug=True)










# # The user details get print in the console.
# # so you can do whatever you want to do instead
# # of printing it

# from flask import Flask, render_template, url_for, redirect

# import os

# app = Flask(__name__)
# app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!/xd5\xa2\xa0\x9fR"\xa1\xa8'

# '''
# 	Set SERVER_NAME to localhost as twitter callback
# 	url does not accept 127.0.0.1
# 	Tip : set callback origin(site) for facebook and twitter
# 	as http://domain.com (or use your domain name) as this provider
# 	don't accept 127.0.0.1 / localhost
# '''

# app.config['SERVER_NAME'] = 'localhost:5000'


# @app.route('/', methods =['GET', 'POST'])
# def index():
# 	return render_template('index123.html')


# if __name__ == "__main__":
# 	app.run(debug=True)
