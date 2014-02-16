from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import db
from DiveBook import app

@app.route('/divesheets/')
def divesheets():
	if 'id' not in session:
		return redirect(url_for('index'))
	sheets = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet','10.0'],[2,'My Other Dive Sheet','Rose-Hulman Dive Meet','10.0']]
	sheets = db.getDiveSheets(session['id'])
	return render_template('divesheets.html',sheets=sheets)

@app.route('/divesheets/<int:id>')
def sheet(id):
	if 'id' not in session:
		return redirect(url_for('index'))
	sheet = [[1,'My Super Awesome Dive Sheet',''],]
	sheet = db.getDiveSheet(id)
	dives = [['A204', '1', 'Forward Dive', 'Tuck', '1.4', '10'],['A204', '1', 'Hurricane Dive', 'Tuck', '1.4', '10']]
	dives=db.getDivesInSheet(id)
	sheet = sheet[0]
	return render_template('divesheet.html', sheet=sheet, dives=dives)

@app.route('/meets/<int:id>/sheet/<int:sheetid>')
def registerMeet(id, sheetid):
	if 'id' not in session:
		return redirect(url_for('index'))
	db.editMeetOfDiveSheets(id, sheetid)
	return redirect(url_for('sheet', id=id))

@app.route('/divesheets/create',methods=['GET','POST'])
def createDiveSheet():
	if 'id' not in session:
		return redirect(url_for('index'))
	message = ""
	# Create default sheet to be created
	sheet = [1,'My Super Awesome Dive Sheet','']
	doableDives = [[1,'Forward Dive','Tuck',1],[2, 'Backward Dive','Tuck',3],[3,'Reverse Hurricane','Tuck',1]]
	doableDives = db.getDoableDives(session['id'])
	dives = []
	if request.method == 'POST':
		if request.form['title']:
			sheet[2] = request.form['title']
		else:
			message = "Title cannot be empty"
		for i in range(1,11):
			if request.form['dive'+str(i)]:
				dives.append(request.form['dive'+str(i)]) # This is an ID
			else:
				message = "Dive number " + str(i) + " cannot be empty!"
		if not message:
			id = 1
			# Commit the sheet to the database, get the id back as id
			id = db.createDiveSheet(sheet, dives, session['id'])
			return redirect(url_for('sheet', id=id))
	return render_template('createdivesheet.html',message=message, sheet=sheet, doableDives=DoableDives)
	
@app.route('/divesheets/<int:id>/edit',methods=['GET','POST'])
def editDiveSheet(id):
	if 'id' not in session:
		return redirect(url_for('index'))
	sheet = [[1,'My Super Awesome Dive Sheet',''],]
	sheet = db.getDiveSheet(id)
	doableDives = [[1,'Forward Dive','Tuck',1],[2, 'Backward Dive','Tuck',3],[3,'Reverse Hurricane','Tuck',1]]
	doableDives = db.getDoableDives(session['id'])
	dives = [1,2,3]
	dives=db.getIdsInSheet(id)
	sheet = sheet[0]
	message = ""
	if request.method == 'POST':
		if request.form['title']:
			sheet[2] = request.form['title']
			# SQL to change the divesheet title
		else:
			message = "Title cannot be empty"
		for i in dives:
			if request.form['dive'+str(i)]:
				dives[i-1] = request.form['dive'+str(i)] # This is an ID
			else:
				message = "Dive number " + str(i) + " cannot be empty!"
		if not message:
			# Commit the sheet to the database, get the id back as id
			db.editDiveSheet(sheet, dives, session['id'])
			return redirect(url_for('sheet', id=id))
	return render_template('editdivesheet.html',message=message, sheet=sheet,dives=dives,doableDives=doableDives)