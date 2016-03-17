import MySQLdb, os, json
from Utility.DBUtility import MySQL

database_name = "CZ4034"
table_name = "CZ4034_originial"

mysql_object = MySQL()

mysql_object.create_database(database_name)

column_list = "DocID TEXT, " \
              "typeOfMaterial TEXT, " \
              "news_desk TEXT, " \
              "headline MEDIUMTEXT, " \
              "lead_paragraph MEDIUMTEXT, " \
              "word_count TEXT,"\
              "publication_date TEXT,"\
              "person TEXT,"\
              "keywords MEDIUMTEXT,"\
              "glocation MEDIUMTEXT,"\
              "section_name TEXT"

mysql_object.create_table(table_name, column_list)

# change the following path accordingly!
path = "../jsonFiles/"
count = 0
x = []
for i in os.listdir(path):
    if (i.endswith(".json")):
        with open(path + "\\" + i) as data_file:
            #if(os.stat(data_file).st_size == 0):
            #    continue
            print(data_file.name)
            data = json.load(data_file)
            for j in range(len(data["response"]["docs"])):

                type_of_material = " "
                lead_paragraph = " "
                pub_date = " "
                section_name = " "
                type_Of_Material = " "
                news_desk = " "
                headline = " "
                word_count= "0"
                people = " "
                keywords = " "
                glocations = " "
                current_response = data["response"]["docs"][j]
                DocId = current_response["_id"]
                if (DocId not in x):
                    x.append(DocId)
                    count += 1
                else:
                    continue

                # checking if type of material exists
                if ('type_of_material' in current_response and current_response["type_of_material"] is not None):
                    type_of_material = current_response["type_of_material"].replace("\"", "\\\"")

                # checking if news desk exists
                if ('news_desk' in current_response and current_response["news_desk"] is not None):
                    news_desk = current_response["news_desk"].replace("\"", "\\\"")

                # checking if print headline and main headline exists
                if ('headline' in current_response):
                    if ('main' in current_response["headline"] and current_response["headline"]["main"] is not None):
                        headline += current_response["headline"]["main"].replace("\"", "\\\"") + " "
                    if ('print_headline' in current_response["headline"] and current_response["headline"]["print_headline"] is not None):
                        headline += current_response["headline"]["print_headline"].replace("\"", "\\\"")

                # checking if word_count exists
                if ('word_count' in current_response and current_response["word_count"] is not None):
                    word_count = str(current_response["word_count"])

                if ((data["response"]['docs'][j]["lead_paragraph"]) is not None):
                    lead_paragraph = data["response"]['docs'][j]["lead_paragraph"].replace("\"", "\\\"")
                elif ((data["response"]['docs'][j]["snippet"]) is not None):
                    lead_paragraph = data["response"]['docs'][j]["snippet"].replace("\"", "\\\"")
                elif ((data["response"]['docs'][j]["abstract"]) is not None):
                    lead_paragraph = data["response"]['docs'][j]["abstract"].replace("\"", "\\\"")
                else:
                    lead_paragraph = headline

                # checking if lead paragraph exists
                if ('lead_paragraph' in current_response and current_response["lead_paragraph"] is not None):
                    lead_paragraph += current_response["lead_paragraph"].replace("\"", "\\\"") + " | "
                if ('snippet' in current_response and current_response["lead_paragraph"] != current_response["snippet"] and current_response["snippet"] is not None):
                    lead_paragraph += current_response["snippet"].replace("\"", "\\\"") + " | "
                if ('abstract' in current_response and current_response["abstract"] is not None and current_response["lead_paragraph"] != current_response["abstract"] and current_response["snippet"] != current_response["abstract"]):
                    lead_paragraph += current_response["abstract"].replace("\"", "\\\"") + " | "

                # checking if publication date exists
                if ('pub_date' in current_response and current_response["pub_date"] is not None):
                    pub_date = current_response["pub_date"][:10]

                # checking if section name exists
                if ('section_name' in current_response and current_response["section_name"] is not None):
                    section_name = current_response["section_name"].replace("\"", "\\\"")

                # checking if by line is empty
                if ('byline' in current_response and ((current_response["byline"]) is not None) and (
                            len((current_response["byline"])) != 0)):
                    for numOfPeople in range(len(current_response["byline"]["person"])):
                        if ('firstname' in current_response["byline"]["person"][numOfPeople]):
                            people += current_response["byline"]["person"][numOfPeople]["firstname"]
                        if ('lastname' in current_response["byline"]["person"][numOfPeople]):
                            people += " " + current_response["byline"]["person"][numOfPeople]["lastname"]
                        people += " | "

                if ('keywords' in current_response and current_response["keywords"] is not None):
                    for numOfKeywords in range(len(current_response["keywords"])):
                        keywords += current_response["keywords"][numOfKeywords]["value"].replace("\"", "\\\"") + " | "
                        if (current_response["keywords"][numOfKeywords]["name"] == "glocations"):
                            glocations += current_response["keywords"][numOfKeywords]["value"].replace("\"", "\\\"") + " | "
                #   print lead_paragraph
                    # print(people[:len(people)-2])
                    # print(keywords[:len(keywords)-2])

                sql = "INSERT INTO " + table_name + " VALUES " \
                       "(\"" + DocId + "\", " \
                       "\"" + type_of_material + "\", " \
                       "\"" + news_desk + "\", " \
                       "\"" + headline + "\", " \
                       "\"" + lead_paragraph + "\", " \
                       "\"" + word_count + "\", " \
                       "\"" + pub_date + "\", " \
                       "\"" + people + "\", " \
                       "\"" + keywords + "\", " \
                       "\"" + glocations + "\", " \
                       "\"" + section_name + "\");"
                try:
                    sql = sql.encode('utf-8')
                    print(sql)
                    mysql_object.execute_query(sql)
                except TypeError as e:
                    # Rollback in case there is any error
                    print(e.message)
                    continue
print(count)
# disconnect from server
mysql_object.close_db()
