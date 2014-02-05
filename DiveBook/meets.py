from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import db
from DiveBook import app

@app.route('/meets/')
def meets():
    upcoming = [[1,'Rose-Hulman','IN','2014-02-19'],]
    past = [[2,'ISU','IN','2014-01-19'],]
    #upcoming = db.getUpcomingMeets()
    #past = db.getPastMeets()
    return render_template('meets.html',upcoming=upcoming,past=past)

@app.route('/meets/<int:id>')
def meet(id):
    meet = [1,'Rose-Hulman Dive Meet', '5500 Wabash Ave','Terre Haute','IN','47803','2014-02-29']
    count = 13
    divesheets = [[1,'Awesome Divesheet'],[2,'Easy Divesheet']]
    #meet,count = db.getMeet(id)
    if 'id' in session:
        divesheets = [[1,'Awesome Divesheet'],[2,'Easy Divesheet']]
        #divesheets = db.getNonRegisteredDiveSheets(session['id'])
    return render_template('meet.html',meet=meet,count=count,divesheets=divesheets)

