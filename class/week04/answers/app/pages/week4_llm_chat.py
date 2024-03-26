import streamlit as st
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from resources import load_openai_llm

col1, col2 = st.columns([4,1])
with col1:
    st.title('Chat with an LLM')
with col2:
    if st.button("Clear Memory"):
        st.session_state.memory.clear()


#### Define the chat history
if "memory" not in st.session_state:
    st.session_state.memory =  ConversationBufferWindowMemory(k=5)

#### Setup prompt templates and conversation objects
TEMPLATE = """TELL THE AI WHO IT IS WITH A SYSTEM MESSAGE

Current conversation:
{history}
Human: {input}
AI:"""

## Create a conversational LLM Chain
if "conversation" not in st.session_state:
    template = TEMPLATE
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    st.session_state.conversation = ConversationChain(
        prompt=PROMPT,
        llm=load_openai_llm(),
        verbose=True,
        memory=st.session_state.memory,
    )

## When a new human chat is received
def next_message(human_input):
    st.session_state.conversation.run(human_input)

## this is the chat input at the bottom of the page
if human_input := st.chat_input("What is up?"):
    next_message(human_input)

#### Loop through the conversation state and create chat messages
with st.container():
    for message in st.session_state.memory.buffer_as_messages:
        with st.chat_message("user" if message.type == 'human' else 'assistant' ):
            st.markdown(message.content)