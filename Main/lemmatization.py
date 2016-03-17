import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import MySQLdb
from Utility.DBUtility import MySQL


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

    mysql_object = MySQL()
    database_name = "CZ4034"

    mysql_object.create_database(database_name)
    tableName = "CZ4034_originial"

    # prepare a cursor object using cursor() method
    sql = "SELECT DocID, headline, lead_paragraph, keywords FROM " + tableName + ";"
    sql = sql.encode('utf-8')
    # Execute the SQL command
    # Commit your changes in the database
    data = mysql_object.execute_query(sql)
    # print(len(data))
    columns = "Token TEXT," \
              "DocID TEXT"

    tableHeadline = "headlineTokens"
    mysql_object.create_table(tableHeadline, columns)
    tableKeywords = "keywordsTokens"
    mysql_object.create_table(tableKeywords, columns)
    tableLeadPara = "leadParagraphTokens"
    mysql_object.create_table(tableLeadPara, columns)
    tableKeywordsMulti = "keywordsMultiWord"
    mysql_object.create_table(tableKeywordsMulti, columns)

    for record in data:
        docID = record[0]
        headline = record[1]
        lead_paragraph = record[2]
        keywords = record[3]

        headline = headline.translate(None, string.punctuation)
        words = word_tokenize(headline)
        headline_withoutStopWords = removeStopWords(words)

        lead_paragraph = lead_paragraph.translate(None, string.punctuation)
        words = word_tokenize(lead_paragraph)
        lead_paragraph_withoutStopWords = removeStopWords(words)

        keyword_list_grams = []
        for keyword in keywords.split(" | "):
            keyword_list_grams.append(
                ((" ".join(removeStopWords(keyword.split(" ")))).strip()).translate(None, string.punctuation))

        keyword_list_grams = filter(None, keyword_list_grams)
        keywords_withoutStopWords = word_tokenize(" ".join(keyword_list_grams))

        
        print(x for x in headline_withoutStopWords)
        # sql = "INSERT INTO "
        print(lead_paragraph_withoutStopWords)
        print(keyword_list_grams)
        print(keywords_withoutStopWords)
        break
