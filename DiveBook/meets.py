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
    #TODO: Pull meet info and populate page
    return render_template('meet.html')

@app.route('/meets/<int:id>/sheet/<int:sheetid>')
def registerMeet(id, sheetid):
    #TODO: Register a sheet
    return "needs html" 