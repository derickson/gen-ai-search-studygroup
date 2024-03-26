import os
import streamlit as st

from elasticsearch import Elasticsearch
from dotenv import load_dotenv


@st.cache_resource
def get_es():
    load_dotenv("../../.env", override=True)

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

    return es

