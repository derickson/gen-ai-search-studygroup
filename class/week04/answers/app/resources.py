import os
import streamlit as st

from elasticsearch import Elasticsearch
from dotenv import load_dotenv


## put at the top of the page
import openai
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv("../../.env", override=True)

## use the @ annotation for a resource so that Streamlit will cache this thing
@st.cache_resource
def load_openai_llm():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    default_model = "gpt-3.5-turbo"
    llm = ChatOpenAI(
        temperature=0.3,
        model=default_model
    )
    return llm


@st.cache_resource
def get_es():
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

