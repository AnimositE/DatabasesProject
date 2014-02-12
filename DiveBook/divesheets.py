from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import db
from DiveBook import app

@app.route('/divesheets/')
def divesheets():
	if 'id' not in session:
		return redirect(url_for('index'))
	sheets = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet','10.0'],]
	return render_template('divesheets.html',sheets=sheets)

@app.route('/divesheets/<int:id>')
def sheet(id):
	if 'id' not in session:
		return redirect(url_for('index'))
    #TODO: Pull meet info and populate page
	sheet = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet',[['A','5','Forward Dive','S','1.4','10','10','10','10','10','10','10','10','10','10'],]],]
	return render_template('divesheet.html', sheet=sheet)

@app.route('/meets/<int:id>/sheet/<int:sheetid>')
def registerMeet(id, sheetid):
	if 'id' not in session:
		return redirect(url_for('index'))
	sheet = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet',[['A','5','Forward Dive','S','1.4','10','10','10','10','10','10','10','10','10','10'],]],]
    # db.editMeetOfDiveSheets(id, sheetid)
	# sheet = db.getDiveSheet(sheetid)
	return render_template('divesheet.html', sheet=sheet)

@app.route('/divesheets/create')
def createDiveSheet():
	if 'id' not in session:
		return redirect(url_for('index'))
	return render_template('createdivesheet.html')
	
@app.route('/divesheets/<int:id>/edit',methods=['GET','POST'])
def editDiveSheet(id):
	if 'id' not in session:
		return redirect(url_for('index'))
	# Find the divesheet id in this list
	# Pass the diverid to the database
	sheet = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet',[['A','5','Forward Dive','S','1.4','10','10','10','10','10','10','10','10','10','10'],]],]
	#sheet = db.getDiveSheets(id) # SQL on divesheet id to get title, dives, etc
	message = ""
	if request.method == 'POST':
		if request.form['title']:
			title = request.form['title'] # This doesnt do shit
			# SQL to change the divesheet title
			# db.?
			return redirect(url_for('sheet', id=id))
		else:
			message = "Title cannot be empty"
	return render_template('editdivesheet.html',message=message, sheet=sheet)