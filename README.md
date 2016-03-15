# CZ4034 Information Retrieval

Open crawl.py and change STATS_FILE_NAME, JSON_FILE_NAME and q. If querying on search term then use q="q=search_term" and if it is a news_desk value then use q="fq=news_desk:(\"value\")".

To check total number of hits till now: awk -F"," '{ sum+=3} END {print sum}' Main/*.csv
