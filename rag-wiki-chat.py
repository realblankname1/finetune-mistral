import dotenv
import os
import streamlit as st

from langchain.retrievers import WikipediaRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

def main():
    st.set_page_config(page_title="AI research agent", page_icon=":bird:")

    st.header("AI research agent :bird:")
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_history = []
        
        retriever = WikipediaRetriever()

        model = ChatOpenAI(model_name="gpt-3.5-turbo")  # switch to 'gpt-4'
        st.session_state.qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("Input Text"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        print(st.session_state.chat_history)
        response = st.session_state.qa({"question": prompt, "chat_history": st.session_state.chat_history})
        st.session_state.chat_history.append((prompt, response["answer"]))
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response["answer"])
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
        
if __name__ == '__main__':
    
    main()