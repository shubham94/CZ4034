from sklearn.svm import SVC
from sklearn import feature_extraction
import string
from Main.Utility.MySQL import MySQL
from Main.lemmatization import lemmatization

lem = lemmatization()
database_name = "cz4034"
table_name = "CZ4034_Originial"
mysql_object = MySQL()
mysql_object.use_database(database_name)

sql = "(SELECT lead_paragraph, news_desk FROM " + table_name + " WHERE news_desk LIKE \"travel\" order by DocID asc  LIMIT 50) " \
      "UNION " \
      "(SELECT lead_paragraph, news_desk FROM " + table_name + " WHERE news_desk LIKE \"dining\" order by DocID asc LIMIT 50) " \
      "UNION " \
      "(SELECT lead_paragraph, news_desk FROM " + table_name + " WHERE news_desk LIKE \"Politics\" order by DocID asc LIMIT 50);"

sql = sql.encode('utf-8')
data = mysql_object.execute_query(sql)

dict = []
categ = []
train_data = []
for record in data:
    train_data.append(record[0])
    ca = record[1]

    if (ca.lower() == "travel"):
        categ.append('Travel')
    elif (ca.lower() == "dining"):
        categ.append('Dining')
    elif (ca.lower() == "politics"):
        categ.append('Politics')

    d = record[0].lower()
    d = d.translate(None, string.punctuation)
    d = lem.removeStopWords(d.split(" "))
    if d not in dict:
        dict.extend(d)

dict = filter(None, list(set(dict)))
print dict

print train_data
model = SVC(kernel='linear', C=1, gamma=1)

cv = feature_extraction.text.CountVectorizer(vocabulary=dict)
X = cv.fit_transform(train_data).toarray()
print categ
model.fit(X, categ)
model.score(X, categ)

sql = "(SELECT lead_paragraph, news_desk FROM " + table_name + " WHERE news_desk LIKE \"Travel\" order by DocID desc  LIMIT 25) " \
      "UNION " \
      "(SELECT lead_paragraph, news_desk FROM " + table_name + " WHERE news_desk LIKE \"dining\" order by DocID desc LIMIT 25) " \
      "UNION " \
      "(SELECT lead_paragraph, news_desk FROM " + table_name + " WHERE news_desk LIKE \"Politics\" order by DocID desc LIMIT 25);"

sql = sql.encode('utf-8')
data = mysql_object.execute_query(sql)
test_data = []
for record in data:
    test_data.append(record[0])

Y = cv.fit_transform(test_data).toarray()
predicted = model.predict(Y)

print(predicted)