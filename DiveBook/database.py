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
    def editprofile(self, newfname, newlname, newage, newdive, diverid):
        self.cursor.execute("UPDATE Profiles SET fName = %s, lName = %s, age = %s, favoriteDive = %s WHERE diverID = %s;", [newfname, newlname,newage,newdive,diverid])
        self.conn.commit()

    def getDivers(self):
        self.cursor.execute("SELECT Divers.id, fName, lName, name FROM Divers, Profiles, Schools WHERE Divers.id = Profiles.diverID AND Profiles.schoolID = Schools.id;")
        return self.cursor.fetchall()

    def getDiverProfile(self, diverid):
        # TODO: pull meets
        self.cursor.execute("SELECT fName, lName, email, age, Schools.name, division, Dives.name FROM Divers JOIN Profiles ON Divers.id = diverID LEFT JOIN Schools ON schoolID = Schools.id LEFT JOIN Dives ON Dives.id = Profiles.favoriteDive WHERE Divers.id = %s;",[diverid])
        return self.cursor.fetchall()

    def getDoableDivesName(self, diverid):
        self.cursor.execute("SELECT name, diveID FROM Doable JOIN Dives ON diveID = id WHERE diverID = %s;",[diverid])
        return self.cursor.fetchall()

    def getMeetsOfDiver(self,diverid):
        self.cursor.execute("SELECT Meets.title FROM Meets, DiveSheets WHERE Meets.id = DiveSheets.meetid AND DiveSheets.diverid = %s;", [diverid])
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
        

    def scoreDives(self, sheetid, row, score):
        self.cursor.execute("UPDATE Scores SET score=%s  WHERE sheetID=%s AND row=%s;",[score,sheetid,row])
        self.conn.commit()


    # --------------------------------------------------------------------------------

    # DIVESHEETS --------------------------------------------------------------------

    def getDiveSheets(self, diverid):
        self.cursor.execute("SELECT Divesheets.id, name, Meets.title, finalScore FROM DiveSheets LEFT JOIN Meets ON meetID=Meets.id WHERE diverID=%s;",[diverid])
        return self.cursor.fetchall()

    def getDiveSheet(self, id):
        self.cursor.execute("SELECT DiveSheets.id, name, title, finalScore FROM DiveSheets LEFT JOIN Meets ON Meets.id=meetID WHERE Divesheets.id=%s;",[id])
        return self.cursor.fetchall()

    def getNonRegisteredDiveSheets(self, diverid):
        self.cursor.execute("SELECT DiveSheets.id, name FROM DiveSheets WHERE diverID=%s AND meetID IS NULL;",[diverid])
        return self.cursor.fetchall()

    def getSheetsForMeet(self, id):
        self.cursor.execute("SELECT DiveSheets.id, name FROM DiveSheets WHERE meetID=%s;",[id])
        return self.cursor.fetchall()

    def createDiveSheet(self, title, dives, diverid):
        self.cursor.execute("INSERT INTO DiveSheets (diverID,name) VALUES (%s,%s) RETURNING Divesheets.id;",[diverid,title])
        id = self.cursor.fetchall()[0]
        for dive in dives:
            self.cursor.execute("INSERT INTO Scores (sheetID,diveID,row) VALUES (%s,%s,%s);",[id,dive[1],dive[0]])
        self.conn.commit()
        return id

    def editDiveSheet(self, sheetid, title, dives, diverid):
        self.cursor.execute("UPDATE DiveSheets SET name=%s WHERE Divesheets.id=%s;",[title, sheetid])
        for dive in dives:
            self.cursor.execute("UPDATE Scores SET diveID=%s WHERE sheetID =%s AND row = %s;",[dive[1],sheetid,dive[0]])
        self.conn.commit()

    def editMeetOfDiveSheet(self, meetid, sheetid):
        self.cursor.execute("UPDATE DiveSheets SET meetID=%s WHERE Divesheets.id=%s;",[meetid,sheetid])
        self.conn.commit()

    def deleteDiveSheet(self, sheetid, diverid):
        self.cursor.execute("DELETE FROM DiveSheets WHERE Divesheets.id=%s AND Divesheets.diverID=%s;",[sheetid,diverid])
        self.conn.commit()

    # -------------------------------------------------------------------------------

    # DIVES ------------------------------------------------------------------------

    def getDD(self, name, height, position):
    	self.cursor.execute("SELECT dd, number FROM Dives WHERE name=%s AND height=%s AND position=%s;",[name, height, position])
    	dd = self.cursor.fetchall()
    	if len(dd) > 0:
    		return dd[0]
    	return ['NOT FOUND', '000']

    def getDoableDive(self, name, height, position):
        self.cursor.execute("SELECT dd, number, id FROM Dives WHERE name=%s AND height=%s AND position=%s;",[name, height, position])
        dd = self.cursor.fetchall()
        if len(dd) > 0:
            return dd[0]
        return ['NOT FOUND', '000', '']

    def addDoable(self, diver, id):
        self.cursor.execute("INSERT INTO Doable (diverID, diveID) SELECT %s, %s WHERE NOT EXISTS (SELECT 1 FROM Doable WHERE diverID=%s AND diveID=%s);",[diver,id,diver,id])
        self.conn.commit()

    def getDives(self):
        self.cursor.execute("SELECT * FROM Dives;")
        return self.cursor.fetchall()

    def getDivesInSheet(self, sheetid):
        self.cursor.execute("SELECT row, number, height, Dives.name, position, dd, score FROM Dives JOIN Scores ON diveID=id JOIN DiveSheets ON sheetID = DiveSheets.id WHERE sheetID=%s ORDER BY row ASC;", [sheetid])
        return self.cursor.fetchall()

    def getIdsInSheet(self, sheetid):
        self.cursor.execute("SELECT diveID FROM Scores WHERE sheetID=%s;", [sheetid])
        return self.cursor.fetchall()

    def getDoableDives(self, diverid):
        self.cursor.execute("SELECT id, name, position, height FROM DoableDives WHERE diverid=%s;", [diverid])
        return self.cursor.fetchall()

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