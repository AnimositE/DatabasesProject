import urlparse
import psycopg2
import os

class Database:

    def __init__(self):
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.conn.cursor()

    def getDivers(self):
        self.cursor.execute("SELECT * FROM Divers;")
        return self.cursor.fetchall()

    # MEETS --------------------------------------------------------------------------

    def getUpcomingMeets(self):
        self.cursor.execute("SELECT id, title, state, date FROM Meets WHERE date > CURRENT_DATE;")
        return self.cursor.fetchall()

    def getPastMeets(self):
        self.cursor.execute("SELECT id, title, state, date FROM Meets WHERE date < CURRENT_DATE;")
        return self.cursor.fetchall()

    # --------------------------------------------------------------------------------

    def getDives(self):
        self.cursor.execute("SELECT * FROM Dives;")
        return self.cursor.fetchall()

    # Account requests ---------------------------------------------------------------

    def login(self, email, password):
    	self.cursor.execute("SELECT id FROM Divers \
    						WHERE email=%s AND hashpass=%s;",[email,password])
    	return self.cursor.fetchall()

    def register(self, email, password):
    	self.cursor.execute("SELECT id FROM Divers WHERE email=%s;",[email])
    	registered =  self.cursor.fetchall()
    	if registered:
    		return False
    	else:
    		self.cursor.execute("INSERT INTO Divers (email, hashpass) VALUES (%s, %s);",[email, password])
    		return True

   	# --------------------------------------------------------------------------------