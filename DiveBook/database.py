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

    # DIVERS ------------------------------------------------------------------------

    def getDivers(self):
        self.cursor.execute("SELECT Divers.id, fName, lName, name FROM Divers, Profiles, Schools WHERE Divers.id = Profiles.diverID AND Profiles.schoolID = Schools.id;")
        return self.cursor.fetchall()

    def getDiverProfile(self, diverid):
        # TODO: pull meets
        self.cursor.execute("SELECT email, fName, lName, age, favoriteDive FROM Divers JOIN Profiles ON id = diverID WHERE id = %s;",[diverid])
        return self.cursor.fetchall()

    def searchDivers(self, fname, lname, school):
        query = "SELECT diverID, fName, lName, name FROM Profiles, Schools WHERE Profiles.schoolID=Schools.id"
        params = []
        if fname != '%%':
            query += " AND LOWER(Profiles.fName) LIKE LOWER(%s)"
            params.append(fname)
        if lname != '%%':
            query += " AND LOWER(Profiles.lName) LIKE LOWER(%s)"
            params.append(lname)
        if school != '%%':
            query += " AND LOWER(Schools.name) LIKE LOWER(%s)"
            params.append(school)
        query += ';'
    	self.cursor.execute(query,params)
    	return self.cursor.fetchall()

    def getDiversAtSchool(self, schoolid):
        self.cursor.execute("SELECT fName, lName FROM Profiles WHERE schoolID=%s;",[schoolid])
        return self.cursor.fetchall()

    def claimDiver(self, email, schoolid):
        self.cursor.execute("SELECT * FROM Divers WHERE email=%s;",[email])
        divers = self.cursor.fetchall()
        if len(divers) == 0:
            return
        self.cursor.execute("UPDATE Profiles SET schoolID=%s WHERE diverID=(SELECT id FROM Divers WHERE email=%s);",[schoolid, email])
        self.conn.commit()

    # -------------------------------------------------------------------------------

    # SCHOOLS ------------------------------------------------------------------------

    def schoolLogin(self, name, password):
        self.cursor.execute("SELECT id FROM Schools \
                            WHERE name=%s AND hashpass=%s;",[name,password])
        return self.cursor.fetchall()

    def schoolInfo(self, schoolid):
        self.cursor.execute("SELECT name, division FROM Schools WHERE id=%s;",[schoolid])
        return self.cursor.fetchall()[0]

    # --------------------------------------------------------------------------------

    # DIVESHEETS --------------------------------------------------------------------

    def getDiveSheets(self, diverid):
        self.cursor.execute("SELECT Divesheets.id, name, Meets.title, finalScore FROM DiveSheets LEFT JOIN Meets ON meetID = Meets.id WHERE diverID=%s;",[diverid])
        return self.cursor.fetchall()

    def getDiveSheet(self, id, sheetid):
        self.cursor.execute("SELECT * FROM DiveSheets WHERE diverID=%s AND id=%s;",[id,sheetid])
        return self.cursor.fetchall()

    def getNonRegisteredDiveSheets(self, diverid):
        self.cursor.execute("SELECT id, name FROM DiveSheets WHERE diverID=%s AND meetID IS NULL;",[diverid])
        return self.cursor.fetchall()

    def getSheetsForMeet(self, id):
        self.cursor.execute("SELECT id, name FROM DiveSheets WHERE meetID=%s;",[id])
        return self.cursor.fetchall()
	
	def createDiveSheet(self, sheet, diverid):
		self.cursor.execute("INSERT INTO DiveSheets(diverID,name) VALUES(%s,%s) RETURNING id;",[diverid,sheet[0][1]])
		id = self.cursor.fetchall()
		for x in range(1,10): #sheet[0][3]
			self.cursor.execute("INSERT INTO Scores(sheetID,diveID) VALUES(%s,%s);",[id,sheet[0][3][x][2]])
		self.conn.commit()
        return id
		
	def editDiveSheeet(self, sheet, diverid):
		self.cursor.execute("INSERT INTO DiveSheets(diverID,name) VALUES(%s,%s) RETURNING id;",[diverid,sheet[0][1]])
		id = self.cursor.fetchall()
		for x in range(1,10): #sheet[0][3]
			self.cursor.execute("INSERT INTO Scores(sheetID,diveID) VALUES(%s,%s);",[id,sheet[0][3][x][2]])
		self.conn.commit()
        return id

    def editMeetOfDiveSheet(self, id, meet):
        self.cursor.execute("UPDATE DiveSheets SET meetID=%s WHERE id=%s;",[meet,id])
        self.conn.commit()
        return self.cursor.fetchall()

    # -------------------------------------------------------------------------------

    # DIVES ------------------------------------------------------------------------

    def getDD(self, name, height, position):
    	self.cursor.execute("SELECT dd, number FROM Dives WHERE name=%s AND height=%s AND position=%s;",[name, height, position])
    	dd = self.cursor.fetchall()
    	if len(dd) > 0:
    		return dd[0]
    	return ['NOT FOUND', '000']

    def getDives(self):
        self.cursor.execute("SELECT * FROM Dives;")
        return self.cursor.fetchall()

    def getDoableDives(self):
        self.cursor.execute("SELECT * FROM DoableDives")

    # -------------------------------------------------------------------------------

    # MEETS --------------------------------------------------------------------------

    def getUpcomingMeets(self):
        self.cursor.execute("SELECT id, title, state, date FROM Meets WHERE date > CURRENT_DATE;")
        return self.cursor.fetchall()

    def getPastMeets(self):
        self.cursor.execute("SELECT id, title, state, date FROM Meets WHERE date < CURRENT_DATE;")
        return self.cursor.fetchall()

    def getMeet(self, id):
        self.cursor.execute("SELECT Meets.id, title, address, city, state, zip, date FROM Meets WHERE Meets.id = %s;",[id])
        meetInfo = self.cursor.fetchall()[0]
        self.cursor.execute("SELECT COUNT(*) FROM Meets, DiveSheets WHERE Meets.id = DiveSheets.meetID AND Meets.id = %s;",[id])
        return meetInfo, self.cursor.fetchall()[0][0]

    def getMeetsForSchool(self, schoolid):
        self.cursor.execute("SELECT id, title FROM Meets WHERE schoolID=%s;",[schoolid])
        return self.cursor.fetchall()

    def createMeet(self,name,address,city,state,zipcode,year,month,day,school):
        datein = year +'-'+month+'-'+day
        self.cursor.execute("INSERT INTO Meets (title,address,city,state,zip,date,schoolID) VALUES (%s,%s,%s,%s,%s,%s,%s);",[name,address,city,state,zipcode,datein,school])
        self.conn.commit()

    # --------------------------------------------------------------------------------

    # Account requests ---------------------------------------------------------------

    def login(self, email, password):
    	self.cursor.execute("SELECT id FROM Divers \
    						WHERE email=%s AND hashpass=%s;",[email,password])
    	return self.cursor.fetchall()

    def register(self, email, password):
        self.cursor.execute("SELECT id FROM Divers WHERE email=%s;",[email])
        registered = self.cursor.fetchall()
        if len(registered) > 0:
            return False
        else:
            self.cursor.execute("INSERT INTO Divers (email, hashpass) VALUES (%s, %s) RETURNING id;",[email, password])
            id = self.cursor.fetchall()[0][0]
            self.cursor.execute("INSERT INTO Profiles (diverID) VALUES (%s);",[id])
            self.conn.commit()
            return True

   	# --------------------------------------------------------------------------------