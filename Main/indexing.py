import pysolr, os, json

solr = pysolr.Solr('http://localhost:8983/solr/', timeout=10)

# If sending JSON files directly into solr

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
            #for j in range(len(data["response"]["docs"])):
            #    current_response = data["response"]["docs"][j]
            solr.add(data["response"]["docs"])
