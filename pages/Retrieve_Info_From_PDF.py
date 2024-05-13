
import streamlit as st
from streamlit import session_state as ss
from openai import OpenAI
import time
api_key = st.secrets["api_key"]

client = OpenAI(api_key=api_key)
st.header('Retrieval of info from PDF files', divider='blue')
st.caption('This GPT4-enabled app uses private PDF files that contains info about Sozcode courses. It can answers your questions on the courses we hold.')

if 'page' not in ss:
    ss.page = "pdf"
    if 'stream' not in ss:
        ss.stream = None
    if "messages" not in ss:
        ss.messages = []
elif ss.page == "csv":
    ss.stream = None
    ss.messages = []
    ss.page = "pdf"
else:
    if 'stream' not in ss:
        ss.stream = None
    if "messages" not in ss:
        ss.messages = []

# variables


# functions
def data_streamer():
    """
    That stream object in ss.stream needs to be examined in detail to come
    up with this solution. It is still in beta stage and may change in future releases.
    """
    for response in ss.stream:
        if response.event == 'thread.message.delta':
            value = response.data.delta.content[0].text.value
            yield value
            time.sleep(0.1)


for message in ss.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# prompt user
if prompt := st.chat_input("What is up?"):
    ss.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    msg_history = [
        {"role": m["role"], "content": m["content"]} for m in ss.messages
    ]

    ss.stream = client.beta.threads.create_and_run(
        assistant_id="asst_WmMWULv2th1lucLFeq4aAvHe",
        thread={
            "messages": msg_history
        },
        stream=True
    )

    with st.chat_message("assistant"):
        response = st.write_stream(data_streamer)
        ss.messages.append({"role": "assistant", "content": response})
