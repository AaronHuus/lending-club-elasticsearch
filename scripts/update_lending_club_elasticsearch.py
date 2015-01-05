import urllib2
import csv
import json
from elasticsearch import Elasticsearch
import logging
import datetime

# Get API Key
with open("api.key") as f:
    api_key = f.read().strip()

# Download current infunding notes from the lending club website
print("Requesting newest notes from Lending club ...")
request = urllib2.Request("https://api.lendingclub.com/api/investor/v1/loans/listing?showAll=True", headers={"Authorization" : api_key})
response = urllib2.urlopen(request)
in_funding_notes = json.load(response)   

# Removing previous in funding loans from elastic search
print("Deleting previous in funding loans from elastic search ...")
es = Elasticsearch()
filter={ "query" : {
        "match" : {
            "_type":"in_funding_note"            
        }
    }
}
es.delete_by_query(index='lending_club', doc_type='in_funding_note', body=filter)

# Adding in funding loans to elasticsearch
print("Adding in funding loans to elastic search ...")
for loan in in_funding_notes['loans']:
    es.index(index='lending_club', doc_type="in_funding_note", body=loan)

print ("Done injesting current Lending Club notes!")
