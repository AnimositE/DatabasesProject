from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for
import hashlib
from DiveBook import db
from DiveBook import app

@app.route('/schools/')
def schools():
	if 'school' in session:
		schoolid = session['school']
		schoolInfo = ['Rose-Hulman', 3]
		meets = [[1,'Rose-Hulman Dive Meet'],]
		divers = [['Mason','Schneider'],]
		schoolInfo = db.schoolInfo(schoolid)
		meets = db.getMeetsForSchool(schoolid)
		divers = db.getDiversAtSchool(schoolid)
		return render_template('schoolprofile.html',schoolInfo=schoolInfo,meets=meets,divers=divers)
	else:
		return render_template('schools.html')

@app.route('/schools/',methods=['POST'])
def schoolLogin():
    name = request.form['school']
    password = hashlib.sha1(request.form['pass']).hexdigest()
    response = [(1,),]
    response = db.schoolLogin(name,password)
    if len(response) != 0:
        session['school'] = response[0][0]
    return redirect(url_for('schools'))

@app.route('/schools/meetinfo/<int:id>')
def schoolMeetInfo(id):
	if 'school' not in session:
		return redirect(url_for('schools'))
	meet = [1,'Rose-Hulman Dive Meet', '5500 Wabash Ave','Terre Haute','IN','47803','2014-02-29']
	count = 13
	divesheets = [[1,'Awesome Divesheet'],[2,'Easy Divesheet']]
	meet,count = db.getMeet(id)
	divesheets = db.getSheetsForMeet(id)
	return render_template('schoolmeetview.html',meet=meet,count=count,divesheets=divesheets)

@app.route('/schools/scoresheet/<int:id>')
def scoreSheet(id):
	return "no bueno"

@app.route('/schools/createmeet/',methods=['GET','POST'])
def createMeet():
	if 'school' not in session:
		return redirect(url_for('schools'))
	message = ''
	if request.method == 'POST':
		name = request.form['name']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		zipcode = request.form['zip']
		year = request.form['year']
		month = request.form['month']
		day = request.form['day']
		school = session['school']
		if name and address and city and state and zipcode and year and month and day:
			if len(year) != 4 or len(day) != 2 or len(month) != 2:
				message = 'Length of dates incorrect'
			else:
				db.createMeet(name,address,city,state,zipcode,year,month,day,school)
				return redirect(url_for('schools'))
		else:
			message = 'All fields are required!'
	return render_template('createmeet.html',message=message)

@app.route('/schools/claimdiver/')
def claimDiver():
	if 'school' not in session:
		return redirect(url_for('schools'))
	return 'no bueno'

@app.route('/schools/logout/')
def schoolLogout():
	if 'school' not in session:
		return redirect(url_for('schools'))
	session.pop('school', None)
	return redirect(url_for('schools'))
