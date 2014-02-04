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

# TODO: Divesheets, schools, doable dives, profile editing, favorite dive

import DiveBook.divers # TODO: Search divers, view a divers profile from session, view from id in url

import DiveBook.meets # TODO: Add single meet view, meet creation, and meet registration

import DiveBook.dd  # complete

import DiveBook.sessions # complete

import DiveBook.divesheets # Mark is mucking around with this