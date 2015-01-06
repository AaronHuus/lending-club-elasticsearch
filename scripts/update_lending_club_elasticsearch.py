import urllib2
import json
from elasticsearch import Elasticsearch
from datetime import datetime
import ConfigParser

# Setup config file and get api and account number
config = ConfigParser.RawConfigParser()
config.read('lc.config')
api_key = config.get("Lending Club","api.key")
account_number = config.get("Lending Club","account")

# Removing previous in funding loans from elastic search
print("Deleting previous in funding loans from elasticsearch ...")
es = Elasticsearch()
in_funding_filter={ "query" : {"match" : {"_type" : "in_funding_note"} } }
es.delete_by_query(index='lending_club', body=in_funding_filter)

# Download current in funding notes from the lending club website
print("Requesting newest notes from Lending club ...")
request = urllib2.Request("https://api.lendingclub.com/api/investor/v1/loans/listing?showAll=True", headers={"Authorization" : api_key})
response = urllib2.urlopen(request)
in_funding_notes = json.load(response)

# Adding in funding loans to elasticsearch
print("Adding in funding loans to elastic search ...")
for loan in in_funding_notes['loans']:
    loan['injestedDate'] = datetime.now()
    es.index(index='lending_club', doc_type="in_funding_note", body=loan)

print ("Done injesting current Lending Club notes!")
