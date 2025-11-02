import streamlit as st
from langgraoh_database_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid
import time
from typing import Iterable

# Page config and top-level heading
st.set_page_config(page_title="LangGraph Chatbot", layout="wide")


# **************************************** utility functions *************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])


def write_stream(generator: Iterable[str], container=None, delay: float = 0.0) -> str:
    """Render a streaming generator into the provided Streamlit container.

    Args:
        generator: an iterable yielding string chunks.
        container: optional Streamlit container (e.g., st.empty()) to write into. If None, a new container is created.
        delay: optional delay between chunks (seconds) to allow UI updates.

    Returns:
        The concatenated string of all chunks.
    """
    if container is None:
        container = st.empty()

    collected = ""
    try:
        for chunk in generator:
            if chunk is None:
                continue
            collected += str(chunk)
            # use markdown to allow basic formatting, but fall back to text if it errors
            try:
                container.markdown(collected)
            except Exception:
                container.text(collected)
            if delay:
                time.sleep(delay)
    except Exception as e:
        # surface errors to the UI in a production-safe way
        container.error(f"Streaming error: {e}")
        raise

    return collected


# **************************************** Session S st.session_state['thread_id']etup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])


# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages


# **************************************** Main UI ************************************

# Main UI headings
st.title('LangGraph Chatbot')
st.header('Conversation')
st.subheader(f'Thread: {st.session_state.get("thread_id")}')

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

     # first add the message to message_history
    with st.chat_message("assistant"):
        # stream assistant response into the chat bubble
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        # create a placeholder inside the chat message and stream into it
        placeholder = st.empty()
        ai_message = write_stream(ai_only_stream(), container=placeholder, delay=0.0)

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})