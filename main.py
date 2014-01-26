import os
from flask import Flask, render_template, send_from_directory
#import database

app = Flask(__name__)
app.config.update(DEBUG = True,)

#db = Database()

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
    return "no html yet"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)