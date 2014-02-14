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
	sheet = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet',[[], ['2','5','Forward Dive','S','1.4','10','10','10','10','10','10','10','10','10','10','100'],]],]
	sheet = db.getDiveSheet(session['id'],id)
	return render_template('divesheet.html', sheet=sheet)

@app.route('/meets/<int:id>/sheet/<int:sheetid>')
def registerMeet(id, sheetid):
	if 'id' not in session:
		return redirect(url_for('index'))
	sheet = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet',[[], ['2','5','Forward Dive','S','1.4','10','10','10','10','10','10','10','10','10','10','100'],]],]
	#db.editMeetOfDiveSheets(id, sheetid)
	#sheet = db.getDiveSheet(sheetid)
	return render_template('divesheet.html', sheet=sheet)

@app.route('/divesheets/create',methods=['GET','POST'])
def createDiveSheet():
	if 'id' not in session:
		return redirect(url_for('index'))
	message = ""
	# Create default sheet to be created
	sheet = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet',[[], ['2','5','Forward Dive','S','1.4','10','10','10','10','10','10','10','10','10','10','100'],]],]
	if request.method == 'POST':
		if request.form['title']:
			sheet[0][2] = request.form['title']
		else:
			message = "Title cannot be empty"
		for i in range(1,11):
			i = str(i)
			if request.form['dive'+i]:
				sheet[0][3][1][0] = request.form['dive'+i]
			else:
				message = "Dive number " + str(i) + " cannot be empty!"
		if not message:
			id = 1
			# Commit the sheet to the database, get the id back as id
			id = db.createDiveSheet(sheet, session['id'])
			return redirect(url_for('sheet', id=id))
	dives = [[1,'Forward Dive','Tuck',1],[2, 'Backward Dive','Tuck',3],[3,'Reverse Hurricane','Tuck',1]]
	# dives = getDives()
	return render_template('createdivesheet.html',message=message, sheet=sheet, dives=dives)
	
@app.route('/divesheets/<int:id>/edit',methods=['GET','POST'])
def editDiveSheet(id):
	if 'id' not in session:
		return redirect(url_for('index'))
	# Find the divesheet id in this list
	# Pass the diverid to the database
	sheet = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet',[[], ['2','5','Forward Dive','S','1.4','10','10','10','10','10','10','10','10','10','10','100'],]],]
	#sheet = db.getDiveSheets(id) # SQL on divesheet id to get title, dives, etc
	message = ""
	if request.method == 'POST':
		if request.form['title']:
			sheet[0][2] = request.form['title']
			# SQL to change the divesheet title
		else:
			message = "Title cannot be empty"
		for i in range(1,11):
			i = str(i)
			if request.form['diveno'+i]:
				sheet[0][3][1][0] = request.form['diveno'+i]
			else:
				message = "Dive number " + str(i) + " cannot be empty!"
			if request.form['level'+i]:
				sheet[0][3][1][1] = request.form['level'+i]
			else:
				message = "Level " + str(i) + " cannot be empty!"
			if request.form['description'+i]:
				sheet[0][3][1][2] = request.form['description'+i]
			else:
				message = "Description " + str(i) + " cannot be empty!"
			if request.form['position'+i]:
				sheet[0][3][1][3] = request.form['position'+i]
			else:
				message = "Position " + str(i) + " cannot be empty!"
			if request.form['dd'+i]:
				sheet[0][3][1][4] = request.form['dd'+i]
			else:
				message = "DD " + str(i) + " cannot be empty!"
		if not message:
			id = 1
			# Commit the sheet to the database, get the id back as id
			#id = db.editDiveSheet(sheet,session['id'])
			return redirect(url_for('sheet', id=id))
	dives = [[1,'Forward Dive','Tuck',1],[2, 'Backward Dive','Tuck',3],[3,'Reverse Hurricane','Tuck',1]]
	dives = db.getDoableDives(session['id'])
	return render_template('editdivesheet.html',message=message, sheet=sheet,dives=dives)