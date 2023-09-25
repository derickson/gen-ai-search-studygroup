import streamlit as st
import json
from resources import get_es
import html

index_name = "genai_state_of_the_union"
size = 5

st.markdown("""<style>
    strong {
        background-color: #FFFF00; /* Bright Yellow */
        color: #000000; /* Black */
    }
</style>""", unsafe_allow_html=True)


# pretty printing JSON objects
def json_pretty(input_object):
  print(json.dumps(input_object, indent=4))

def custom_escape(text):
    # First, we HTML escape the entire text
    escaped = html.escape(text)
    # Then, we unescape our desired patterns
    escaped = escaped.replace("&lt;strong&gt;", "<strong>")
    escaped = escaped.replace("&lt;/strong&gt;", "</strong>")
    return escaped

def runKeywordSearch(input):
    es = get_es()

    query = {
        "query_string": {
        "query": input,
        "default_field": "*"
        }
    }
    
    source_fields = ["administration","url","date"]

    highlight = {
        "fields": {"text": {}},
        "pre_tags": ["<strong>"],
        "post_tags": ["</strong>"]
    }

    response = es.search(
        index=index_name, 
        query=query, 
        source=source_fields,
        highlight=highlight,
        size=size)
    
    print(json_pretty(response.body))

    st.session_state.search_results = response["hits"]

"## State of the Union Search"
col1, col2 = st.columns([6,1])
with col1:
    keyword_search_box = st.text_input("Search Input", "")
with col2:
    ""
    ""
    if st.button("🔎", type="secondary", key="searchKeyword"): 
        ""
        # countDocs()   
        runKeywordSearch(keyword_search_box)

st.markdown("<hr/>", unsafe_allow_html=True)

if "search_results" in st.session_state :
    "Search Results"
    results = st.session_state.search_results
    hit_count = results["total"]["value"]
    result_count = len(results["hits"])

    f"Results {result_count} of {hit_count}"

    for result in results["hits"]:
        url = result["_source"]["url"]
        date = result["_source"]["date"]
        administration = result["_source"]["administration"]
        st.markdown(f"<h2><a href='{url}'>{date} - {administration}</a></h2>",unsafe_allow_html=True)
        html_composite = "<p>"
        for hl in result["highlight"]["text"]:
            html_composite = html_composite + "<br/>" + custom_escape(hl)
        html_composite = html_composite + "</p>"
        st.markdown(html_composite, unsafe_allow_html=True)
