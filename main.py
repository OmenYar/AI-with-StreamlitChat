import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import(
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title = "AI Chat by Bachtiar",
        page_icon = "🤖"
    )

def main():
    
    init()

    st.markdown("<h3 style='text-align: center; color: white;'>AI Chat with Streamlit-Chat 🤖</h3>", unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: white;'>Built by <a href='https://github.com/OmenYar'>Bachtiar ❤️</a> </h6>", unsafe_allow_html=True)

    chat = ChatOpenAI(temperature=0)

    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="Kamu adalah Asisten dari Bachtiar.")
        ]

    response_container = st.container()
    form_container = st.container()

    with form_container:
        with st.form(key="my-form", clear_on_submit=True):
            user_input = st.text_input("Pesan Anda:", placeholder="Masukkan Pesan yang ingin Anda Sampaikan", key="user_input")
            submit_button = st.form_submit_button(label="Kirim")
            
            if submit_button and user_input:
                st.session_state.messages.append(HumanMessage(content=user_input))
                
                with st.spinner("In Progress..."):
                    response = chat(st.session_state.messages)
                
                st.session_state.messages.append(AIMessage(content=response.content))


    with response_container:
        messages = st.session_state.get('messages', [])
        for i, msg in enumerate(messages[1:]):
            if i % 2 == 0:
                message(msg.content, is_user=True, key=str(i) + '_user')
            else:
                message(msg.content, is_user=False, key=str(i) + '_ai')

if __name__ == '__main__':
    main()