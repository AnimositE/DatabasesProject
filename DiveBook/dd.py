from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import app
from DiveBook import db

@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Error 418:</h1><br><img src="http://images.sodahead.com/polls/000635829/polls_teapot_1856_35455_poll_xlarge.jpeg">', 418

@app.route('/dd/')
def ddLookup():
    return render_template('ddlookup.html')

@app.route('/dd/',methods=['POST'])
def ddPost():
    height = request.form['height']
    group = request.form['group']
    dive = request.form['dive']
    twist = request.form['twist']
    position = request.form['position']
    name = group + ' ' + dive
    if twist != '0':
        name += ' ' + twist
    diveInfo = [1.4,'101']
    diveInfo = db.getDD(name,height,position)
    return render_template('ddlookup.html',name=name,height=height,dd=diveInfo[0],number=diveInfo[1],position=position)

@app.route('/dives/',methods=['GET','POST'])
def doables():
    if 'id' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        height = request.form['height']
        group = request.form['group']
        dive = request.form['dive']
        twist = request.form['twist']
        position = request.form['position']
        name = group + ' ' + dive
        if twist != '0':
            name += ' ' + twist
        diveInfo = [1.4,'101',1]
        diveInfo = db.getDoableDive(name,height,position)
        return render_template('doable.html',name=name,height=height,dd=diveInfo[0],number=diveInfo[1],position=position,id=diveInfo[2])
    return render_template('doable.html')

@app.route('/doable/<int:id>')
def doableAdd(id):
    if 'id' not in session:
        return redirect(url_for('index'))
    diver = session['id']
    db.addDoable(diver,id)
    return redirect(url_for('viewprofile'))
