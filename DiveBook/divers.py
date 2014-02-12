from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import db
from DiveBook import app

@app.route('/divers/')
def divers():
    divers = [[1,'Mason','Schneider','Rose-Hulman'],[2,'Mark','Hein','Rose-Hulman']]
    #divers = db.getDivers()
    return render_template('divers.html',divers=divers)

@app.route('/divers/',methods=['POST'])
def searchDivers():
    fname = '%' + request.form['first'] + '%'
    lname = '%' + request.form['last'] + '%'
    school = '%' + request.form['school'] + '%'
    divers = [[1,'Mason','Schneider','Rose-Hulman'],]
    #divers = db.searchDivers(fname, lname, school)
    return render_template('divers.html',divers=divers)

@app.route('/profile/<int:id>')
def profile(id):
    #TODO: Generate profile page from diver id
    return render_template('profile.html',profile=profile)

@app.route('/profile/')
def viewprofile():
    if 'id' not in session:
        return redirect(url_for('index'))
    #TODO: Generate profile page from diver id
    return render_template('profile.html',profile=profile)