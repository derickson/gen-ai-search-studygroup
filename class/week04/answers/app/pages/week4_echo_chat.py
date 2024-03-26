import streamlit as st

"# Echo"

#### Define the chat history
if "echo_memory" not in st.session_state:
    st.session_state.echo_memory =  []

#### Setup prompt templates and conversation objects
## TODO

## This is what to do when a new human input chat is received
def next_message(human_input):
    st.session_state.echo_memory.append({"role":"user","message":human_input})
    st.session_state.echo_memory.append({"role":"ai","message":human_input})

## this is the chat input at the bottom of the page
if human_input := st.chat_input("What is up?"):
    next_message(human_input)

#### Loop through the conversation state and create chat messages
with st.container():
    for msg in st.session_state.echo_memory:
        with st.chat_message(msg["role"]):
            st.write(msg["message"])