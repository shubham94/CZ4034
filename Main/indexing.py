import pysolr, os, json

solr = pysolr.Solr('http://localhost:8983/solr/test', timeout=10)

#Delete existing indexed json files in solr
solr.delete(q='*:*')

# If sending JSON files directly into solr

path = "../jsonFiles/"
count = 0
x = []
for i in os.listdir(path):
    if (i.endswith(".json")):
        with open(path + i) as data_file:
            #if(os.stat(data_file).st_size == 0):
            #    continue
            print(data_file.name)
            data = json.load(data_file)
            for j in range(len(data["response"]["docs"])):
                jsondata = {}
                current_response = data["response"]["docs"][j]
                DocId = current_response["_id"]
                if (DocId not in x):
                    x.append(DocId)
                    jsondata["DocId"] = DocId
                    print(DocId)
                    count += 1
                else:
                    continue
                #print current_response
                # checking if news desk exists
                if ('news_desk' in current_response and current_response["news_desk"] is not None):
                    jsondata["news_desk"] = current_response["news_desk"]

                # checking if print headline and main headline exists
                if ('headline' in current_response and current_response["headline"] is not None):
                    jsondata["headline"] = current_response["headline"]

                # checking if lead paragraph exists
                if ('lead_paragraph' in current_response and current_response["lead_paragraph"] is not None):
                    jsondata["lead_paragraph"] = current_response["lead_paragraph"]

                if ('keywords' in current_response and current_response["keywords"] is not None):
                    jsondata["keywords"] = current_response["keywords"]
                #print jsondata
                solr.add([jsondata])
            solr.commit()

results = solr.search('health')
for result in results:
    print(result)
