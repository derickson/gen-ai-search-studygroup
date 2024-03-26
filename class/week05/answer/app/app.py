import streamlit as st
import json
from resources import get_es
import html

index_name = "genai_state_of_the_union"
size = 5

st.set_page_config(layout="wide")


if "facet_selections" not in st.session_state:
    st.session_state.facet_selections = {}

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

    queries = []
    
    if input.strip() != "":
        queries.append({
            "query_string": {
                "query": input,
                "default_field": "*"
            }
        })
    else:
        queries.append({"match_all": {}})

    for key in st.session_state.facet_selections:
        if st.session_state.facet_selections[key]:
            field, value = key.split("|")
            term_query = {"term": {field: value}}
            queries.append(term_query)

    query = {"bool":{"must":queries}}

    aggs = {
        "administration_facets": {
            "terms": {
                "field": "administration" 
            }
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
        aggregations=aggs,
        source=source_fields,
        highlight=highlight,
        size=size)
    
    print(json_pretty(response.body))

    st.session_state.search_results = response["hits"]
    st.session_state.search_aggs = response["aggregations"]

"## State of the Union Search"
col1, col2 = st.columns([6,1])
with col1:
    keyword_search_box = st.text_input("Search Input", "")
with col2:
    ""
    ""
if st.button("🔎", type="secondary", key="searchKeyword"): 
        ""
        st.session_state.facet_selections = {}
        runKeywordSearch(keyword_search_box)

st.markdown("<hr/>", unsafe_allow_html=True)

if "search_results" in st.session_state :
    "Search Results"
    results = st.session_state.search_results
    hit_count = results["total"]["value"]
    result_count = len(results["hits"])

    f"Results {result_count} of {hit_count}"

    r1, r2 = st.columns([1,3])
    with r1:
        aggs = st.session_state.search_aggs if "search_aggs" in st.session_state else {}
        change_detected = False
        for key in aggs:
            field_name = key.replace("_facets","")
            f"#### {field_name}"
            for bucket in aggs[key]["buckets"]:
                facet_value = bucket['key']
                doc_count = bucket['doc_count']
                facet_index = f"{field_name}|{facet_value}"
                
                ## the checkbox
                checkbox = st.checkbox(f"{facet_value} ({doc_count})", key=facet_index)
                ## grab the current value from session state so we can detect change
                cur_val = facet_index in st.session_state.facet_selections and st.session_state.facet_selections[facet_index] 
                ## Based on the value, which may include the user just having changed it, set state and detect change
                if checkbox:
                    st.session_state.facet_selections[facet_index] = True
                    if not cur_val:
                        change_detected = True
                else:
                    st.session_state.facet_selections[facet_index] = False
                    if cur_val:
                        change_detected = True

        if change_detected:            
            runKeywordSearch(keyword_search_box)
            st.rerun()

    with r2:
        for result in results["hits"]:
            url = result["_source"]["url"]
            date = result["_source"]["date"]
            administration = result["_source"]["administration"]
            st.markdown(f"<h2><a href='{url}'>{date} - {administration}</a></h2>",unsafe_allow_html=True)
            html_composite = "<p>"
            if "highlight" in result:
                for hl in result["highlight"]["text"]:
                    html_composite = html_composite + "<br/>" + custom_escape(hl)
            else:
                html_composite = html_composite + "No highlights<br/>"
            html_composite = html_composite + "</p>"
            st.markdown(html_composite, unsafe_allow_html=True)
