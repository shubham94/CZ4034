import os, json

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
                #                if (len((data["response"]["docs"][j]["byline"])) != 0):
                if (((data["response"]["docs"][j]["byline"]) is not None) and (
                    len((data["response"]["docs"][j]["byline"])) != 0)):
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

