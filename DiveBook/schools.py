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
		#schoolInfo = db.schoolInfo(schoolid)
		#meets = db.getMeetsForSchool(schoolid)
		#divers = db.getDiversAtSchool(schoolid)
		return render_template('schoolprofile.html',schoolInfo=schoolInfo,meets=meets,divers=divers)
	else:
		return render_template('schools.html')

@app.route('/schools/',methods=['POST'])
def schoolLogin():
    name = request.form['school']
    password = hashlib.sha1(request.form['pass']).hexdigest()
    response = [(1,),]
    #response = db.schoolLogin(name,password)
    if len(response) != 0:
        session['school'] = response[0][0]
    return redirect(url_for('schools'))

@app.route('/schools/meetinfo/<int:id>')
def schoolMeetInfo(id):
	return 'nothing yet'

@app.route('/schools/createmeet/')
def createMeet():
	return 'nothing here'

@app.route('/schools/claimdiver/')
def claimDiver():
	return 'no bueno'
