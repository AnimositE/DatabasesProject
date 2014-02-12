from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import app
from DiveBook import db

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
    #diveInfo = db.getDD(name,height,position)
    return render_template('ddlookup.html',name=name,height=height,dd=diveInfo[0],number=diveInfo[1],position=position)