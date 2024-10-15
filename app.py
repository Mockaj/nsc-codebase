# app.py
import streamlit as st
from langtail_api import create_thread, delete_thread, list_threads, send_message
import json

st.set_page_config(page_title="Chat with NonStop Consulting CRM Codebase 🧠", page_icon="💬", layout="wide")

st.title("Chat with NonStop Consulting CRM Codebase 🧠")

# Initialize session state variables
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None

if 'threads' not in st.session_state:
    st.session_state.threads = []

if 'messages' not in st.session_state:
    st.session_state.messages = []

def refresh_threads():
    try:
        threads = list_threads()
        st.session_state.threads = threads.get('threads', [])
    except Exception as e:
        st.error(f"Failed to refresh threads: {e}")

# Refresh threads on first load
if not st.session_state.threads:
    refresh_threads()

# Sidebar for thread management
with st.sidebar:
    st.header("Chats")
    # Display existing threads
    thread_ids = [thread.get('id') for thread in st.session_state.threads]
    selected_thread = st.selectbox("Select a chat", options=thread_ids, index=0 if thread_ids else -1)

    if st.button("Refresh chats"):
        refresh_threads()
        st.rerun()

    if st.button("New chat"):
        try:
            new_thread = create_thread()
            st.session_state.thread_id = new_thread['id']
            st.session_state.messages = []
            refresh_threads()
            st.rerun()
        except Exception as e:
            st.error(f"Failed to create a new chat: {e}")

    if st.button("Delete chat"):
        if st.session_state.thread_id:
            try:
                delete_thread(st.session_state.thread_id)
                st.session_state.thread_id = None
                st.session_state.messages = []
                refresh_threads()
                st.rerun()
            except Exception as e:
                st.error(f"Failed to delete the chat: {e}")
        else:
            st.warning("No chat selected to delete.")

    # Set the current thread_id based on selection
    if selected_thread:
        if st.session_state.thread_id != selected_thread:
            st.session_state.thread_id = selected_thread
            # Optionally, load messages for the thread
            st.session_state.messages = []

# Main chat interface
if st.session_state.thread_id:
    st.subheader(f"Chat ID: {st.session_state.thread_id}")
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # Accept user input
    if prompt := st.chat_input("Type your message"):
        # Add user message to session state
        user_message = {'role': 'user', 'content': prompt}
        st.session_state.messages.append(user_message)
        with st.chat_message('user'):
            st.markdown(prompt)

        # Send message to assistant without streaming
        try:
            response = send_message(
                thread_id=st.session_state.thread_id,
                messages=[user_message]
            )

            # Extract assistant's response from the JSON response
            assistant_response_content = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

            if assistant_response_content:
                # Add assistant's message to session state
                assistant_message = {'role': 'assistant', 'content': assistant_response_content}
                st.session_state.messages.append(assistant_message)
                with st.chat_message('assistant'):
                    st.markdown(assistant_response_content)
            else:
                st.warning("Received an empty response from the assistant.")

        except Exception as e:
            st.error(f"Failed to get a response from the assistant: {e}")

else:
    st.write("Please select or create a chat from the sidebar.")