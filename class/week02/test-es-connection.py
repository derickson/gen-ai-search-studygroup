import os
from dotenv import load_dotenv
load_dotenv(".env", override=True)

from elasticsearch import Elasticsearch

es = None

if 'ELASTIC_CLOUD_ID' in os.environ:
  es = Elasticsearch(
    cloud_id=os.environ['ELASTIC_CLOUD_ID'],
    basic_auth=(os.environ['ELASTIC_USER'], os.environ['ELASTIC_PASSWORD']),
    request_timeout=30
  )
elif 'ELASTIC_URL' in os.environ:
  es = Elasticsearch(
    os.environ['ELASTIC_URL'],
    basic_auth=(os.environ['ELASTIC_USER'], os.environ['ELASTIC_PASSWORD']),
    request_timeout=30
  )
else:
  print("env needs to set either ELASTIC_CLOUD_ID or ELASTIC_URL")

if es:
    print(es.info()['tagline']) # should return cluster info