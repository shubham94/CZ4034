from Utility.MySQL import MySQL

database_name = "CZ4034"
table_name = "CZ4034_Original"
mysql_object = MySQL()

mysql_object.use_database(database_name)

sql = "SELECT lead_paragraph, news_desk FROM " + table_name + " WHERE news_desk LIKE \"%fitness\""