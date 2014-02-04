import os
from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for
#from database import Database

db = ""
#db = Database()

app = Flask(__name__)
app.config.update(DEBUG = True,)
app.secret_key = 'A0Zz98j/3yX R~XHH!?1N]LWX/,?RT'  #Temp secret


@app.route('/')
@app.route('/index/')
def index():
    return render_template('home.html')

import DiveBook.divers

import DiveBook.meets

import DiveBook.dd

import DiveBook.sessions