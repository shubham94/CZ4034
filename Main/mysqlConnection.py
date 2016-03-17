import MySQLdb, os, json
username = "root"
password = "12345"
database = "CZ4034"
tableName = "testRun"

# Open databas connection
db = MySQLdb.connect("localhost", username, password, "information_schema")

# prepare a cursor object using cursor() method
cursor = db.cursor()
sql = "USE " + database + ";"
cursor.execute(sql)
query = "select headline, lead_paragraph, keywords from testrun where docID = '568e53c57988104ebd4960c3'"
print query
sql = query.encode('utf-8')
# Execute the SQL command
cursor.execute(sql)
# Commit your changes in the database
data = cursor.fetchall()
print data


