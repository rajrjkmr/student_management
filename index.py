from flask import Flask,escape,render_template,url_for,request,redirect,make_response,session
import MySQLdb,time
import datetime
app=Flask(__name__)
app.secret_key = "raj"
def test(data):
	con=MySQLdb.connect("localhost","root","root","test")
	obj=con.cursor()
	ttime=datetime.datetime.now().strftime("%y-%m-%d:   %H-%M-%S")

	data=obj.execute("INSERT INTO hello(`command`,`time`,`like_v`,`dlike_v`) VALUES ('%s','%s','%d','%d')" % (data,ttime,0,0))
	con.commit()
	con.close()
def sign_up_login(name,email,password,college,date,gender,contact_no):
	con=MySQLdb.connect("localhost","root","root","test")
	obj=con.cursor()
	ttime=datetime.datetime.now().strftime("%y-%m-%d:   %H-%M-%S")
	data=obj.execute("INSERT INTO login(`name`,`email`,`password`,`college`,`date`,`gender`,`contact_no`,`reg`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (name,email,password,college,date,gender,contact_no,ttime))

	con.commit()
	con.close()
	

@app.route("/command")
def command():
	da=[]
	sa=[]
	con=MySQLdb.connect("localhost","root","root","test")
	obj=con.cursor()
	obj.execute("SELECT *FROM hello")
	data=obj.fetchall()
	# for data in data:
	# 	for data in data:
	# 		da.append(data)		
	
	con.close()
	
	return render_template("new.html",data=data)
@app.route("/store",methods=['POST','GET'])
def store():
	data=request.form["data"]
	test(data)
	return redirect("/command")

@app.route("/like/<value>")
def like(value):
	con=MySQLdb.connect("localhost","root","root","test")
	obj=con.cursor()
	obj.execute("SELECT like_v FROM hello WHERE s_no='%s'" %(value))
	pre=obj.fetchone()
	for pre in pre:
		print pre
	
	add=pre+1
	obj.execute("UPDATE hello SET like_v ='%s' WHERE s_no='%s';" %(add,value)) 
	con.commit()
	con.close()
	return redirect("/command")


@app.route("/dlike/<value>")
def dlike(value):
	con=MySQLdb.connect("localhost","root","root","test")
	obj=con.cursor()
	obj.execute("SELECT dlike_v FROM hello WHERE s_no='%s'" %(value))
	pre=obj.fetchone()
	for pre in pre:
		print pre
	
	add=pre+1
	obj.execute("UPDATE hello SET dlike_v ='%s' WHERE s_no='%s';" %(add,value)) 
	con.commit()
	con.close()
	return redirect("/command")
@app.route("/sign_in")
def sign_in():
	return render_template("sign_in.html")

@app.route("/validate", methods=["POST","GET"])
def validate():
	res=make_response()
	user_name=request.form["user_name"]
	password=request.form["password"]
	session['user_name']=user_name
	con=MySQLdb.connect("localhost","root","root","test")
	obj=con.cursor()
	data=obj.execute("SELECT *FROM login WHERE email='%s' && password='%s'" %(user_name,password))
	
	if data==0:
		error="Invalide User Register"
		return render_template("sign_up.html",error=error)
	else:
		return redirect("/view")
		# set_cookie('user_name',user_name)
		
@app.route("/view")
def view():
	if 'user_name' in session:
		user_name=session['user_name']
		print user_name
		con=MySQLdb.connect("localhost","root","root","test")
		obj=con.cursor()
		obj.execute("SELECT *FROM login WHERE email='%s'" %(user_name))
		data=obj.fetchone()
		user=obj.fetchall()
		return render_template("view.html",data=data,user=user)
		
	return redirect("/sign_in")
	

@app.route("/profile")
def profile():
	if user_name=='':
		return redirect("/sign_in")
	else:		
		con=MySQLdb.connect("localhost","root","root","test")
		obj=con.cursor()
		obj.execute("SELECT *FROM login WHERE email='%s'" %(user_name))
		data=obj.fetchone()
		return render_template("profile.html",data=data)





@app.route("/sign_up")
def sign_up():
	return render_template("sign_up.html")
@app.route("/sign_up_store",methods=["GET","POST"])
def sign_up_store():
	name=request.form["name"]
	email=request.form["emailid"]
	password=request.form["password"]
	cpassword=request.form["cpassword"]
	college=request.form["college"]
	date=request.form["date"]
	gender=request.form["gender"]
	contact_no=request.form["contact_no"]
	# file_name=request.form["file_name"]
	sign_up_login(name,email,password,college,date,gender,contact_no)
	return render_template("/index.html")
@app.route("/logout")
def logout():
	session.pop('user_name', None)
	return redirect("/")
	
@app.route("/")
def index():
	return render_template("index.html")


if __name__=="__main__":
	app.run()		
