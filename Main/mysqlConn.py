import MySQLdb, os, json

username = "root"
password = "12345"
database = "CZ4034"
tableName = "testRun"

# Open database connection
db = MySQLdb.connect("localhost", username, password, "information_schema")

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "CREATE DATABASE IF NOT EXISTS " + database + ";"

try:
    cursor.execute(sql)
    sql = "USE " + database + ";"
    cursor.execute(sql)
except:
    print("error in creating the database")
    exit(-1)
# Prepare SQL query to INSERT a record into the database.
sql = "CREATE TABLE IF NOT EXISTS " + tableName + " (\
 DocID VARCHAR(200),\
 typeOfMaterial VARCHAR(20),\
 news_desk VARCHAR(20),\
 headline VARCHAR(1000),\
 lead_paragraph VARCHAR(10000),\
 print_page INTEGER,\
 publication_date VARCHAR(100),\
 person VARCHAR(500),\
 keywords VARCHAR(1000),\
 section_name VARCHAR(50)\
 );"
print(sql)
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()

# change the following path accordingly!
path = "../jsonFiles/"
count = 0
x = []
for i in os.listdir(path):
    if (i.endswith(".json")):
        with open(path + "\\" + i) as data_file:
            print(data_file.name)
            data = json.load(data_file)
            for j in range(len(data["response"]["docs"])):
                DocId = data["response"]["docs"][j]["_id"]
                if (DocId not in x):
                    x.extend(DocId)
                    count += 1
                else:
                    continue
                type_of_material = data["response"]["docs"][j]["type_of_material"]
                news_desk = data["response"]["docs"][j]["news_desk"]
                headline = data["response"]["docs"][j]["headline"]["main"]
                print_page = str(data["response"]["docs"][j]["print_page"])
                if (print_page == "None"):
                    print_page = "0"
                if ((data["response"]['docs'][j]["lead_paragraph"]) is not None):
                    lead_paragraph = data["response"]['docs'][j]["lead_paragraph"]
                elif ((data["response"]['docs'][j]["snippet"]) is not None):
                    lead_paragraph = data["response"]['docs'][j]["snippet"]
                elif ((data["response"]['docs'][j]["abstract"]) is not None):
                    lead_paragraph = data["response"]['docs'][j]["abstract"]
                else:
                    lead_paragraph = headline

                pub_date = data["response"]["docs"][j]["pub_date"]
                section_name = data["response"]["docs"][j]["section_name"]
                word_count = data["response"]["docs"][j]["word_count"]
                people = ""
                keywords = ""
                try:
                    if (len((data["response"]["docs"][j]["byline"])) != 0):
                        for numOfPeople in range(len(data["response"]["docs"][j]["byline"]["person"])):
                            if (('firstname' in data["response"]["docs"][j]["byline"]["person"][numOfPeople]) & (
                                        'lastname' in data["response"]["docs"][j]["byline"]["person"][
                                        numOfPeople])):
                                people += data["response"]["docs"][j]["byline"]["person"][numOfPeople][
                                              "firstname"] + " " + \
                                          data["response"]["docs"][j]["byline"]["person"][numOfPeople][
                                              "lastname"] + ", "
                    for numOfKeywords in range(len(data["response"]["docs"][j]["keywords"])):
                        keywords += data["response"]["docs"][j]["keywords"][numOfKeywords]["name"] + ": " + \
                                    data["response"]["docs"][j]["keywords"][numOfKeywords]["value"] + ", "
                        # print(people[:len(people)-2])
                        # print(keywords[:len(keywords)-2])
                    sql = "INSERT INTO " + tableName + " VALUES (\"" + DocId + "\",\"" + type_of_material + "\", \"" + \
                          news_desk + "\", \"" + headline + "\", \"" + \
                          lead_paragraph + "\", " + print_page + ", \"" + \
                          pub_date + "\", \"" + people + "\", \"" + \
                          keywords + "\", \"" + section_name + "\");"
                    sql = sql.encode('utf-8')
                    print(sql)
                    try:
                        # Execute the SQL command
                        cursor.execute(sql)
                        # Commit your changes in the database
                        db.commit()
                        print("added")
                    except MySQLdb.MySQLError as e:
                        # Rollback in case there is any error
                        print(e.message)
                        db.rollback()
                except:
                    #Random command
                    a = 1

print(count)
# disconnect from server
db.close()
