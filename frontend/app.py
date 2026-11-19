import streamlit as st
import requests
import os
from uuid import uuid4

API_URL = os.getenv('API_URL','http://127.0.0.1:8000')
st.set_page_config(
    page_title='Research Buddy',
    page_icon='😈',
    layout='wide'
)
if 'message' not in st.session_state:
    st.session_state.message = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'session_id' not in st.session_state:
    st.session_state.session_id=str(uuid4())
st.title('Your AI Research Assistant')
st.write('Research Buddy is an interactive AI tool that cuts short your studying time so you can jump straight to the most important part')

with st.sidebar:
    st.header('Functions')
    uploaded_files = st.file_uploader(
        label='Select a file',
        type=['pdf','txt'],
        accept_multiple_files=True
    )
    st.subheader('Uploaded Documents')
    for name in st.session_state.uploaded_files:
        st.write(name)
    if st.button('Clear Chat'):
        st.session_state.message = []
        st.rerun()

if uploaded_files and st.button('Upload'):
    for uploaded_file in uploaded_files:
        try:
            response = requests.post(
                f'{API_URL}/upload',
                files={
                    'file':(
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }
            )
            response.raise_for_status()
            result = response.json()
            st.session_state.uploaded_files.append(uploaded_file.name)
            st.success(
                f'{uploaded_file.name} uploaded successfully '
                f"{result['chunks']} chunks created"
            )
        except requests.RequestException as e:
            st.error(f'Upload failed: {e}')
    st.rerun()
st.divider()
st.subheader('Ask about your documents')

for message in st.session_state.message:
    with st.chat_message(message['role']):
        st.write(message['content'])
        if message['role'] == 'assistant':
            for source in message.get('sources',[]):
                st.markdown(
                    f"**{source['source']}** —"
                    f"Page {source['page'] or 'N/A'} ({source['id']})"
                )

query = st.chat_input("What'd you like to know?")

if query:
    with st.spinner('Hmmmmm lemme think....'):
        try:
            response = requests.post(
                f'{API_URL}/ask',
                json={'query': query}
            )
            response.raise_for_status()
            result = response.json()

            st.session_state.message.append({
                'role':'user',
                'content':query
            })

            st.session_state.message.append({
                'role':'assistant',
                'content':result['response'],
                'sources':result['source']
            })
            st.rerun()

            
        except requests.RequestException as e:
            st.error(f'Failed to get an answer: {e}')