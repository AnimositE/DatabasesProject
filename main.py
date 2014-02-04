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


# Divers ------------------------------------------------------------------------------

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

# -------------------------------------------------------------------------------------+

# Meet viewing and registration --------------------------------------------------------

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

# --------------------------------------------------------------------------------------+

# DD lookup -----------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------------+

#  Diver registration and logging ---------------------------------------------------------

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

#--------------------------------------------------------------------------------------------+

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)