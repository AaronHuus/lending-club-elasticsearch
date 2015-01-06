import urllib2
import json
from elasticsearch import Elasticsearch
from datetime import datetime
import ConfigParser

# Setup config file and get api and account number
config = ConfigParser.RawConfigParser()
config.read('lc.config')
api_key = config.get("Lending Club","api.key")
account_number = config.get("Lending Club","account.number")
account_nickname = config.get("Lending Club","account.name")

# Removing previous in funding loans from elastic search
print("Deleting previous owned loans from elasticsearch ...")
es = Elasticsearch()
owned_filter={ "query" : {"match" : {"_type" : "owned_note"} } }
es.delete_by_query(index='lending_club', body=owned_filter)

# Download current in funding notes from the lending club website
print("Requesting owned notes from Lending club ...")
request = urllib2.Request("https://api.lendingclub.com/api/investor/v1/accounts/%s/notes" % account_number, headers={"Authorization" : api_key})
response = urllib2.urlopen(request)
owned_notes = json.load(response)

# Adding in funding loans to elasticsearch
print("Adding in funding loans to elastic search ...")
for loan in owned_notes['myNotes']:
    loan['injestedDate'] = datetime.now()
    loan ['accountNickname'] = account_nickname
    es.index(index='lending_club', doc_type="owned_note", body=loan)

print ("Done injesting currently owned Lending Club notes!")
