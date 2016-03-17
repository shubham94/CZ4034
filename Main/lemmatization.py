import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import MySQLdb


class lemmatiization:
    def removeStopWords(words):
        line = []
        stop_words = set(stopwords.words("english"))
        for w in words:
            if w not in stop_words:
                line.append(w)
        return line

    def getBiwords(words):
        bigrams_val = nltk.bigrams(words)
        biwords = []
        for word in bigrams_val:
            biwords.append(word)
        return biwords

    username = "root"
    password = "12345"
    database = "CZ4034"
    tableName = "testRun"

    # Open database connection
    db = MySQLdb.connect("localhost", username, password, "CZ4034")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    query = "select headline, lead_paragraph, keywords from testrun"
    sql = query.encode('utf-8')
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    data = cursor.fetchall()
    print(len(data))
    for x in data:
        headline = x[0]
        lead_paragraph = x[1]
        keywords = x[2].split(" | ")

        headline = headline.translate(None, string.punctuation)
        words = word_tokenize(headline)
        headline_withoutStopWords = removeStopWords(words)

        lead_paragraph = lead_paragraph.translate(None, string.punctuation)
        words = word_tokenize(lead_paragraph)
        lead_paragraph_withoutStopWords = removeStopWords(words)

        keywords = keywords.translate(None, string.punctuation)
        words = word_tokenize(keywords)
        keywords_withoutStopWords = removeStopWords(words)
        keywords_biWords = getBiwords(keywords_withoutStopWords)



        print(headline_withoutStopWords)
        print(lead_paragraph_withoutStopWords)
        print(keywords_withoutStopWords)
        print(keywords_biWords)
        break
