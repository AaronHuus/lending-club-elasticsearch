import urllib2
import csv
import json
from elasticsearch import Elasticsearch
import logging
import datetime
import subprocess

# Download historical loan data from Lending Club
subprocess.call(['./download_historical_note_data.sh'])

# Delete old lending_club index from Elastic search
es = Elasticsearch()
es.indices.delete(index='lending_club', ignore=[400, 404])

# Historical data injested from each CSV file into elasticsearch
filenames = ['LoanStats3a_securev1.csv','LoanStats3b_securev1.csv','LoanStats3c_securev1.csv']
for filename in filenames:
    print('Adding notes from %s to elastic search' % filename)
    with open('../historical_data/%s' % filename, 'rb') as notes:
        note_reader = csv.reader(notes, delimiter=',', quotechar='"')
        headers = next(note_reader)
        for note_entry in note_reader:
            note = {"source" : filename }
            for header, field in zip(headers,note_entry):
		try:
	        	note[header] = datetime.datetime.strptime(field.strip(), '%b-%Y').strftime('%Y-%m-01') 
        	except: 
            		try:
                		note[header] = float(field.strip())
	            	except:
				if field.strip() == '':
                    			note[header] = None
                		else:
                    			note[header] = field.strip()
            es.index(index='lending_club', doc_type="note", body=note)
print ("Done injesting historical Lending Club data!")
