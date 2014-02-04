from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import db
from DiveBook import app

@app.route('/divesheets/')
def divesheets():
    sheets = [[1,'My Super Awesome Dive Sheet','Rose-Hulman Dive Meet','10.0'],]
    return render_template('divesheets.html',sheets=sheets)

@app.route('/divesheets/<int:id>')
def sheet(id):
    #TODO: Pull meet info and populate page
	info = [[1,'A',5,'Forward Dive','S',1.4]]
	return render_template('divesheet.html', info=info)

# Registering divesheets should be done through meets