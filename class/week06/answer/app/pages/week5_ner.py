import streamlit as st
from annotated_text import annotated_text
from resources import get_es

import re

def annotated_entity_to_list_of_tuples(message_ner):
    # Pattern to capture content inside [text](label&value)
    pattern = r'\[(.*?)\]\((.*?)&(.*?)\)'
    
    result = []
    last_end = 0

    # Iterating over each match
    for match in re.finditer(pattern, message_ner):
        # Getting start and end index of match
        start, end = match.span()
        
        # If there's text before the match, add it to result
        if start != last_end:
            result.append((message_ner[last_end:start]))
        
        # Add the matched tuple
        label, value = match.groups()[1], match.groups()[0]
        result.append((value, label))
        
        last_end = end
    
    # If there's remaining text after the last match, add it to result
    if last_end != len(message_ner):
        result.append((message_ner[last_end:]))

    return result



def process_ner(text_input):
    es = get_es()

    docs = [{ "_source": {"message": text_input}}]
    infrence = es.ingest.simulate(id='week5_ner', docs=docs)
    message_ner = infrence["docs"][0]["doc"]["_source"]["message_ner"]

    list_of_results = annotated_entity_to_list_of_tuples(message_ner)
    return list_of_results


"# Named Entity Recognition"

text_area = st.text_area("Text to analyze with NER")

if text_area:
    st.divider()
    processed_text = process_ner(text_area)
    annotated_text(processed_text)