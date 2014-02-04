import hashlib
from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for

from DiveBook import db
from DiveBook import app

@app.route('/register/',methods=['GET','POST'])
def register():
    message = ""
    if request.method == 'POST':
        if request.form['email'] and request.form['pass'] and request.form['conf']:
            if request.form['pass'] == request.form['conf']:
                email = request.form['email']
                password = hashlib.sha1(request.form['pass']).hexdigest()
                registered = True
                #registered = db.register(email, password)
                if registered:
                    login()
                else:
                    message = "Email already registered"
            else:
                message = "Passwords do not match"
        else:
            message = "No field can be left empty"
    return render_template('register.html',message=message)


@app.route('/login/',methods=['POST'])
def login():
    email = request.form['email']
    password = hashlib.sha1(request.form['pass']).hexdigest()
    response = [(1,),]
    #response = db.login(email,password)
    if len(response) == 0:
        return redirect(url_for('index'))
    else:
        session['id'] = response[0][0]
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))