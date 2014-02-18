from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import db
from DiveBook import app

@app.route('/divers/')
def divers():
    divers = [[1,'Mason','Schneider','Rose-Hulman'],[2,'Mark','Hein','Rose-Hulman']]
    divers = db.getDivers()
    return render_template('divers.html',divers=divers)

@app.route('/divers/',methods=['POST'])
def searchDivers():
    fname = '%' + request.form['first'] + '%'
    lname = '%' + request.form['last'] + '%'
    school = '%' + request.form['school'] + '%'
    divers = [[1,'Mason','Schneider','Rose-Hulman'],]
    divers = db.searchDivers(fname, lname, school)
    return render_template('divers.html',divers=divers)

@app.route('/profile/<int:id>')
def profile(id):
    profile = [['Thelonius','Coco Diver', 'coco@ilovediving.com', '2', 'Rose-Hulman', 'I', 'Back Tuck'],]
    doabledives = [['Forward Dive'], ['Back Tuck'], ['Front 1 1/2']]
    profile = db.getDiverProfile(id)
    profile = profile[0]
    doabledives = db.getDoableDivesName(id)
    meets = [['Home Meet'], ['Franklin'], ['Washington']]
    meets = db.getMeetsOfDiver(id)
    return render_template('profile.html',profile=profile, doabledives=doabledives, meets=meets)

@app.route('/profile/')
def viewprofile():
    if 'id' not in session:
        return redirect(url_for('index'))
    diverid = session['id']
    profile = [['Thelonius','Coco Diver', 'coco@ilovediving.com', '2', 'Rose-Hulman', 'I', 'Back Tuck'],]
    doabledives = [['Forward Dive'], ['Back Tuck'], ['Front 1 1/2']]
    profile = db.getDiverProfile(diverid)
    profile = profile[0]
    doabledives = db.getDoableDivesName(diverid)
    meets = [['Home Meet'], ['Franklin'], ['Washington']]
    meets = db.getMeetsOfDiver(diverid)
    return render_template('profile.html',profile=profile, doabledives=doabledives, meets=meets)

@app.route('/manageprofile/',methods=['GET','POST'])
def editprofile():
    if 'id' not in session:
        return redirt(url_for('index'))
    diverid = session['id']
    profile = [['Thelonius','Coco Diver', 'coco@ilovediving.com', '2', 'Rose-Hulman', 'I', 'Back Tuck'],]
    doabledives = [['Forward Dive'], ['Back Tuck'], ['Front 1 1/2']]
    #profile = db.getDiverProfile(diverid)
    profile = profile[0]
    #doabledives = db.getDoableDivesName(diverid)
    meets = [['Home Meet'], ['Franklin'], ['Washington']]
    #meets = db.getMeetsOfDiver(diverid)
    return render_template('profileedit.html',profile=profile, doabledives=doabledives, meets=meets)


