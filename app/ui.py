import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent / "app"))
from agent import agent

st.set_page_config(page_title="Airport Assistant", page_icon="✈️")
st.title("✈️ Airport Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask about flights, baggege, transport..."):
    st.session_state.messages.append({"role":"user", "content" : prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = agent.invoke({"messages": st.session_state.messages})
            reply = result["messages"][-1].content
        st.markdown(reply)
    st.session_state.messages.append({"role":"assistant","content":reply})
