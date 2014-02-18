from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import db
from DiveBook import app

@app.route('/divesheets/')
def divesheets():
	if 'id' not in session:
		return redirect(url_for('index'))
	sheets = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet','10.0'],[2,'My Other Dive Sheet','Rose-Hulman Dive Meet','10.0']]
	#sheets = db.getDiveSheets(session['id'])
	return render_template('divesheets.html',sheets=sheets)

@app.route('/divesheets/<int:id>')
def sheet(id):
	if 'id' not in session:
		return redirect(url_for('index'))
	sheet = [[1,'My Super Awesome Dive Sheet',''],]
	#sheet = db.getDiveSheet(id)
	sheet = sheet[0]
	dives = [[1, 'A204', '1', 'Forward Dive', 'Tuck', '1.4', '10'],[2, 'A204', '1', 'Hurricane Dive', 'Tuck', '1.4', '10']]
	#dives = db.getDivesInSheet(id)
	return render_template('divesheet.html', sheet=sheet, dives=dives)

@app.route('/meets/<int:meetid>/sheet/<int:sheetid>')
def registerMeet(meetid, sheetid):
	if 'id' not in session:
		return redirect(url_for('index'))
	#db.editMeetOfDiveSheet(meetid, sheetid)
	return redirect(url_for('sheet', id=sheetid))

@app.route('/divesheets/<int:id>/delete/')
def deleteSheet(id):
	if 'id' not in session:
		return redirect(url_for('index'))
	#db.deleteDiveSheet(id, session['id'])
	return redirect(url_for('divesheets'))

@app.route('/divesheets/create',methods=['GET','POST'])
def createDiveSheet():
	if 'id' not in session:
		return redirect(url_for('index'))
	message = ""
	# Create default sheet to be created
	title = None
	doableDives = [[1,'Forward Dive','Tuck',1],[2, 'Backward Dive','Tuck',3],[3,'Reverse Hurricane','Tuck',1]]
	#doableDives = db.getDoableDives(session['id'])
	dives = []
	if request.method == 'POST':
		if request.form['title']:
			title = request.form['title']
		else:
			message = "Title cannot be empty"
		for i in range(1,11):
			if request.form['dive'+str(i)]:
				dives.append([i, request.form['dive'+str(i)]]) # [row, dive id]
			else:
				message = "Dive number " + str(i) + " cannot be empty!"
		if not message:
			id = [1]
			# Commit the sheet to the database, get the id back as id
			#id = db.createDiveSheet(title, dives, session['id'])
			return redirect(url_for('sheet', id=id[0]))
	return render_template('createdivesheet.html',message=message, title=title, dives=dives, doableDives=doableDives)
	
@app.route('/divesheets/<int:id>/edit',methods=['GET','POST'])
def editDiveSheet(id):
	if 'id' not in session:
		return redirect(url_for('index'))
	sheet = [[1,'My Super Awesome Dive Sheet',''],]
	#sheet = db.getDiveSheet(id)
	sheet = sheet[0]
	title = sheet[1]
	sheetid = sheet[0]
	doableDives = [[1,'Forward Flop','A',1],]
	#doableDives = db.getDoableDives(session['id'])
	dives = ([2],[1],[2],[1],[1],[1],[1],[1],[1],[1])
	#dives=db.getIdsInSheet(id)
	dives = list(dives)
	message = ""
	if request.method == 'POST':
		dives = []
		title = None
		if request.form['title']:
			title = request.form['title']
		else:
			message = "Title cannot be empty"
		for i in range(1,11):
			if request.form['dive'+str(i)]:
				dives.append([i, request.form['dive'+str(i)]]) # [row, dive id]
			else:
				message = "Dive number " + str(i) + " cannot be empty!"
		if not message:
			# Commit the sheet to the database, get the id back as id
			#db.editDiveSheet(sheetid, title, dives, session['id'])
			return redirect(url_for('sheet', id=id))
	return render_template('editdivesheet.html',message=message, title=title, sheetid=sheetid,dives=dives,doableDives=doableDives)

@app.route('/schools/scoresheet/<int:id>',methods=['GET','POST'])
def editScoresOfDiveSheet(id):
	if 'school' not in session:
		return redirect(url_for('schools'))
	message = ""
	sheet = [[1,'My Super Awesome Dive Sheet','The Meet Name'],]
	#sheet = db.getDiveSheet(id)
	sheet=sheet[0]
	dives = [[1, 'A204', '1', 'Forward Dive', 'Tuck', '1.4', '20'],[2, 'A204', '1', 'Hurricane Dive', 'Tuck', '1.4', ''],[1, 'A204', '1', 'Forward Dive', 'Tuck', '1.4', '20'],[2, 'A204', '1', 'Hurricane Dive', 'Tuck', '1.4', ''],[1, 'A204', '1', 'Forward Dive', 'Tuck', '1.4', '20'],[2, 'A204', '1', 'Hurricane Dive', 'Tuck', '1.4', ''],[1, 'A204', '1', 'Forward Dive', 'Tuck', '1.4', '20'],[2, 'A204', '1', 'Hurricane Dive', 'Tuck', '1.4', ''],[1, 'A204', '1', 'Forward Dive', 'Tuck', '1.4', '20'],[2, 'A204', '1', 'Hurricane Dive', 'Tuck', '1.4', ''],]
	#dives = getDivesInSheet(id)
	if request.method == 'POST':
		newdives=[]
		# Check that every field was entered in
		for i in range(1,11):
			if request.form['dive'+str(i)]:
				newdives.append(request.form['dive'+str(i)]) # [row, score]
			else:
				message = 'Dive ' + str(i) + ' score field cannot be empty!'
		print message
		if not message:
			# For each dive returned, set the score of that dive equal to the score
			for i in range(1,11):
				#db.scoreDives(id,i,newdives[i-1])
				pass
			return redirect(url_for('schools'))
	return render_template('scores.html', sheet=sheet, dives=dives, message=message)