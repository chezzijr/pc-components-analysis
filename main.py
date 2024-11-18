import asyncio
import logging
from langchain.schema import AIMessage, HumanMessage
import streamlit as st
import os
from populate import insert_components, insert_prices
from settings import settings
from chat import rag_chain

# stdout as the default logging handler
logfile = "log.txt"
logging.basicConfig(
    filename=logfile,
    filemode="a",
    format="%(asctime)s - %(name)s [%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

if not settings.ignore_insert_components:
    insert_components()
    # set env
    os.environ["ignore_insert_components"] = "true"
if not settings.ignore_insert_prices:
    asyncio.run(insert_prices())
    os.environ["ignore_insert_prices"] = "true"

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

chain = rag_chain.pick("answer")
st.set_page_config(page_title="PC Components Assistant")
st.title("Say something...")
messages = st.container()
for message in st.session_state["chat_history"]:
    if isinstance(message, HumanMessage):
        messages.chat_message("user").write(message.content)
    elif isinstance(message, AIMessage):
        messages.chat_message("assistant").write(message.content)

if prompt := st.chat_input("Say something"):
    messages.chat_message("user").write(prompt)
    with st.spinner("Generating response..."):
        resp = messages.chat_message("assistant").write_stream(
            chain.stream({"input": prompt, "chat_history": st.session_state["chat_history"]})
        )
    st.session_state["chat_history"].extend([
        HumanMessage(content=prompt),
        AIMessage(content=resp),
    ])
