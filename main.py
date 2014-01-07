import os
from flask import Flask
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["ec2-54-197-241-78.compute-1.amazonaws.com"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

app = Flask(__name__)

@app.route('/')
def index():
    cursor = conn.cursor()
    #cursor.execute("SELECT * FROM Users")
    #users = cursor.fetchall()
    return 'Connected!'