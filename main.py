import os
from flask import Flask, render_template, send_from_directory
"""import urlparse
import psycopg2

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)"""

app = Flask(__name__)
app.config.update(DEBUG = True,)

@app.route('/')
@app.route('/index/')
def index():
    #cursor = conn.cursor()
    #cursor.execute("SELECT * FROM Diver")
    #users = cursor.fetchall()
    return render_template('home.html')

@app.route('/divers/')
def divers():
    return render_template('divers.html')

@app.route('/meets/')
def meets():
    return "no html yet"

@app.route('/dd/')
def ddLookup():
    return "no html yet"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)