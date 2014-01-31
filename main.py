import os
import hashlib
from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for
#from database import Database

#db = Database()

app = Flask(__name__)
app.config.update(DEBUG = True,)
app.secret_key = 'A0Zz98j/3yX R~XHH!?1N]LWX/,?RT'  #Temp secret


@app.route('/')
@app.route('/index/')
def index():
    return render_template('home.html')

@app.route('/divers/')
def divers():
    #divers = db.getDivers()
    return render_template('divers.html')

@app.route('/meets/')
def meets():
    #meets = db.getMeets()
    return render_template('meets.html')

@app.route('/dd/')
def ddLookup():
    #dives = db.getDives()
    return render_template('ddlookup.html')

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
    #response = db.login(email,password)
    response = [(1,),]
    if len(response) == 0:
        return redirect(url_for('index'))
    else:
        session['id'] = response[0][0]
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)