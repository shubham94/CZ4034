import pysolr, os, json
from nltk.corpus import wordnet as wn
from Main.lemmatization import lemmatization
from itertools import chain
import simplejson
from urllib2 import urlopen

solr = pysolr.Solr('http://localhost:8983/solr/test', timeout=10)

lem = lemmatization()

query="obesity and heart"
queryLst = lem.lemmatizeWord(lem.removeStopWords(query.lower().split(" ")))
print "query list: \n"
print queryLst
resplst=set()
url="http://localhost:8983/solr/test/select?q="

#keyword AND search#############################
for word in queryLst:
    #url+="%2Bkeywords:*\:*" + word + "*+"
    url+="%2Bkeywords:*\:*" + word[0].upper() + word[1:] + "*+"
url = url[:-1]
url+="&wt=json&rows=15"
print "url: " + url

conn = urlopen(url)
rsp = simplejson.load(conn)
print rsp
for result in rsp["response"]["docs"]:
     print(result)
     resplst.add(result["docID"][0])

##headline AND search #############################

url="http://localhost:8983/solr/test/select?q="

for word in queryLst:
    #url+="%2Bheadline:*\:*" + word + "*+"
    url+="%2Bheadline:*\:*" + word[0].upper() + word[1:] + "*+"

url = url[:-1]
url+="&wt=json&rows=15"
print "url: " + url


conn = urlopen(url)
rsp = simplejson.load(conn)
print rsp
for result in rsp["response"]["docs"]:
     print(result)
     resplst.add(result["docID"][0])

print resplst

##keyword + headline OR #############################

url="http://localhost:8983/solr/test/select?q="

for word in queryLst:
    #url+="headline:*\:*" + word + "*+" + "keywords:*\:*" + word + "*+"
    url+="headline:*\:*" + word[0].upper() + word[1:] + "*+" + "keywords:*\:*" + word[0].upper() + word[1:] + "*+"

url = url[:-1]
url+="&wt=json&rows=15"
print "url: " + url


conn = urlopen(url)
rsp = simplejson.load(conn)
print rsp
for result in rsp["response"]["docs"]:
     print(result)
     resplst.add(result["docID"][0])

print resplst

##phrase search #############################


url="http://localhost:8983/solr/test/select?q=headline:*\:\""

for word in queryLst:
    #url+= word + "+"
    url+=word[0].upper() + word[1:] + "+"

url = url[:-1]
url+="\"&wt=json&rows=15"
print "url: " + url

conn = urlopen(url)
rsp = simplejson.load(conn)
print rsp
for result in rsp["response"]["docs"]:
     print(result)
     resplst.add(result["docID"][0])

print resplst

## SYNONYM headline OR search


print "New list"
for item in queryLst:
    synonyms = wn.synsets(item)
    lst = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    url="http://localhost:8983/solr/test/select?q="
    for word in lst:
        #url+="%2Bheadline:*\:*" + word + "*+"
        url+="headline:*\:*" + word[0].upper() + word[1:] + "*+"

    url = url[:-1]
    url+="&wt=json&rows=15"
    print "url: " + url

    conn = urlopen(url)
    rsp = simplejson.load(conn)
    print rsp
    for result in rsp["response"]["docs"]:
         print(result)
         resplst.add(result["docID"][0])

    print resplst


print resplst.__len__()
# If sending JSON files directly into solr
"""

# How you'd index data.
solr.delete(q='*:*')
testJson = {
    "type_of_material": "Blog",
        "blog": [],
        "news_desk": "Science",
        "lead_paragraph": None,
        "headline": {
          "main": "Mexican Soda Tax Followed by Drop in Sugary Drink Sales",
          "kicker": "Well"
        },
        "abstract": "A tax on sugary drinks in Mexico appears to have had a significant impact: After one year, a new study found, sales of sugary beverages in Mexico fell while bottled water purchases rose.",
        "print_page": None,
        "word_count": "914",
        "_id": "568da4167988104ebd495f23",
        "snippet": "A tax on sugary drinks in Mexico appears to have had a significant impact: After one year, a new study found, sales of sugary beverages in Mexico fell while bottled water purchases rose.",
        "source": "The New York Times",
        "slideshow_credits": None,
        "web_url": "http://well.blogs.nytimes.com/2016/01/06/mexican-soda-tax-followed-by-drop-in-sugary-drink-sales/",
        "multimedia": [
          {
            "subtype": "wide",
            "url": "images/2016/01/07/science/wellmexico/wellmexico-thumbWide.jpg",
            "height": 126,
            "width": 190,
            "legacy": {
              "wide": "images/2016/01/07/science/wellmexico/wellmexico-thumbWide.jpg",
              "wideheight": "126",
              "widewidth": "190"
            },
            "type": "image"
          },
          {
            "subtype": "xlarge",
            "url": "images/2016/01/07/science/wellmexico/wellmexico-articleLarge.jpg",
            "height": 400,
            "width": 600,
            "legacy": {
              "xlargewidth": "600",
              "xlarge": "images/2016/01/07/science/wellmexico/wellmexico-articleLarge.jpg",
              "xlargeheight": "400"
            },
            "type": "image"
          },
          {
            "subtype": "thumbnail",
            "url": "images/2016/01/07/science/wellmexico/wellmexico-thumbStandard.jpg",
            "height": 75,
            "width": 75,
            "legacy": {
              "thumbnailheight": "75",
              "thumbnail": "images/2016/01/07/science/wellmexico/wellmexico-thumbStandard.jpg",
              "thumbnailwidth": "75"
            },
            "type": "image"
          }
        ],
        "subsection_name": None,
        "keywords": [
          {
            "value": "Obesity",
            "name": "subject",
            "rank": "1"
          },
          {
            "value": "Sales and Excise Taxes",
            "name": "subject",
            "rank": "2"
          },
          {
            "value": "Soft Drinks",
            "name": "subject",
            "rank": "3"
          },
          {
            "value": "Sugar",
            "name": "subject",
            "rank": "4"
          }
        ],
        "byline": {
          "person": [
            {
              "organization": "",
              "role": "reported",
              "rank": 1,
              "firstname": "Anahad",
              "lastname": "O'CONNOR"
            }
          ],
          "original": "By ANAHAD O'CONNOR"
        },
        "document_type": "blogpost",
        "pub_date": "2016-01-06T18:30:27Z",
        "section_name": "Health"
      }

print [testJson]

solr.add([testJson])



testJson = {
        "type_of_material": "Blog",
        "blog": [],
        "news_desk": "Science",
        "lead_paragraph": None,
        "headline": {
          "main": "New Dietary Guidelines Urge Less Sugar for All and Less Protein for Boys and Men",
          "kicker": "Well",
          "print_headline": "New Dietary Guidelines Urge Sharp Cuts in Sugar "
        },
        "abstract": "New federal dietary guidelines announced on Thursday urge Americans to drastically cut back on sugar, and for the first time have singled out teenage boys and men for eating too much meat.",
        "print_page": None,
        "word_count": "1150",
        "_id": "568e53c57988104ebd4960c3",
        "snippet": "New federal dietary guidelines announced on Thursday urge Americans to drastically cut back on sugar, and for the first time have singled out teenage boys and men for eating too much meat.",
        "source": "The New York Times",
        "slideshow_credits": None,
        "web_url": "http://well.blogs.nytimes.com/2016/01/07/new-diet-guidelines-urge-less-sugar-for-all-and-less-meat-for-boys-and-men/",
        "multimedia": [
          {
            "subtype": "wide",
            "url": "images/2016/01/06/health/well_food/well_food-thumbWide.jpg",
            "height": 126,
            "width": 190,
            "legacy": {
              "wide": "images/2016/01/06/health/well_food/well_food-thumbWide.jpg",
              "wideheight": "126",
              "widewidth": "190"
            },
            "type": "image"
          },
          {
            "subtype": "xlarge",
            "url": "images/2016/01/06/health/well_food/well_food-articleLarge.jpg",
            "height": 397,
            "width": 600,
            "legacy": {
              "xlargewidth": "600",
              "xlarge": "images/2016/01/06/health/well_food/well_food-articleLarge.jpg",
              "xlargeheight": "397"
            },
            "type": "image"
          },
          {
            "subtype": "thumbnail",
            "url": "images/2016/01/06/health/well_food/well_food-thumbStandard.jpg",
            "height": 75,
            "width": 75,
            "legacy": {
              "thumbnailheight": "75",
              "thumbnail": "images/2016/01/06/health/well_food/well_food-thumbStandard.jpg",
              "thumbnailwidth": "75"
            },
            "type": "image"
          }
        ],
        "subsection_name": None,
        "keywords": [
          {
            "value": "Jacobson, Michael F",
            "name": "persons",
            "rank": "1"
          },
          {
            "value": "Nestle, Marion",
            "name": "persons",
            "rank": "2"
          },
          {
            "value": "United States",
            "name": "glocations",
            "rank": "1"
          },
          {
            "value": "Diet and Nutrition",
            "name": "subject",
            "rank": "1"
          },
          {
            "value": "Eggs",
            "name": "subject",
            "rank": "2"
          },
          {
            "value": "Food",
            "name": "subject",
            "rank": "3"
          },
          {
            "value": "Lunch and Breakfast Programs",
            "name": "subject",
            "rank": "4"
          },
          {
            "value": "Meat",
            "name": "subject",
            "rank": "5"
          },
          {
            "value": "Men and Boys",
            "name": "subject",
            "rank": "6"
          },
          {
            "value": "Sugar",
            "name": "subject",
            "rank": "7"
          }
        ],
        "byline": {
          "person": [
            {
              "organization": "",
              "role": "reported",
              "rank": 1,
              "firstname": "Anahad",
              "lastname": "O'CONNOR"
            }
          ],
          "original": "By ANAHAD O'CONNOR"
        },
        "document_type": "blogpost",
        "pub_date": "2016-01-07T07:00:09Z",
        "section_name": "Health"
      }

test = {"type_of_material" :testJson["type_of_material"] , "news_desk":testJson["news_desk"] }
test["pub"] = testJson["pub_date"]
print test
solr.add([test])
solr.commit()

# Later, searching is easy. In the simple case, just a plain Lucene-style
# query is fine.

results = solr.search('Obesity')
for result in results:
    print(result)

"""

#(q='headline:*Obesity* AND keywords:*Obesity* AND wt=json AND rows=15')

"""
solr.delete(q='*:*')

"""


