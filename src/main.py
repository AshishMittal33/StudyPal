import os
import streamlit as st
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory

from chatbot_utility import get_chapter_list
from get_yt_video import get_yt_video_link

# -------------------- ENV --------------------
load_dotenv()

working_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(working_dir)

# -------------------- CONSTANTS --------------------
subjects_list = ["Biology","Physics"]

# -------------------- HELPERS --------------------
def get_vector_db_path(chapter, subject):
    if chapter == "All Chapters":
        return f"{parent_dir}/vector_db/class_12/{subject.lower()}/_vector_db"
    return f"{parent_dir}/chapters_vector_db/{chapter}"

def setup_chain(selected_chapter, selected_subject):
    """Create and return ConversationalRetrievalChain"""

    vector_db_path = get_vector_db_path(selected_chapter, selected_subject)

    embeddings = HuggingFaceEmbeddings(model_kwargs={"device": "cpu"})

    vectorstore = Chroma(
        persist_directory=vector_db_path,
        embedding_function=embeddings
    )

    llm = ChatGroq(
        model="llama-3.1-8b-instant",  # ✅ SAFE & FAST
        temperature=0.1
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3}
        ),
        memory=memory,
        return_source_documents=True,
        verbose=False
    )

    return chain  # ✅ VERY IMPORTANT


# -------------------- STREAMLIT CONFIG --------------------
st.set_page_config(
    page_title="StudyPal",
    page_icon="📚",
    layout="centered",
)

st.title("📚 StudyPal – Chapter-wise AI Tutor")

# -------------------- SESSION STATE --------------------
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("video_history", [])
st.session_state.setdefault("chat_chain", None)
st.session_state.setdefault("selected_chapter", None)

# -------------------- SUBJECT SELECTION --------------------
selected_subject = st.selectbox(
    "Select Subject (Class 12)",
    options=subjects_list,
    index=None
)

# -------------------- CHAPTER SELECTION --------------------
if selected_subject:
    chapter_list = get_chapter_list(selected_subject) + ["All Chapters"]

    selected_chapter = st.selectbox(
        f"Select Chapter – {selected_subject}",
        options=chapter_list
    )

    # Reset chain ONLY if chapter changes
    if selected_chapter != st.session_state.selected_chapter:
        st.session_state.chat_chain = setup_chain(
            selected_chapter,
            selected_subject
        )
        st.session_state.chat_history = []
        st.session_state.video_history = []
        st.session_state.selected_chapter = selected_chapter

# -------------------- DISPLAY CHAT HISTORY --------------------
for idx, msg in enumerate(st.session_state.chat_history):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant" and idx < len(st.session_state.video_history):
            video_refs = st.session_state.video_history[idx]
            if video_refs:
                st.subheader("🎥 Video References")
                for title, link in video_refs:
                    st.info(f"{title}\n\n🔗 {link}")

# -------------------- USER INPUT --------------------
user_input = st.chat_input("Ask your question...")

if user_input:
    if st.session_state.chat_chain is None:
        st.error("Please select a subject and chapter first.")
        st.stop()

    # USER MESSAGE
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    st.session_state.video_history.append(None)

    with st.chat_message("user"):
        st.markdown(user_input)

    # ASSISTANT RESPONSE
    with st.chat_message("assistant"):
        response = st.session_state.chat_chain.invoke({
            "question": user_input
        })

        answer = response["answer"]
        st.markdown(answer)

        # YOUTUBE REFERENCES
        search_query = ", ".join(
            msg["content"]
            for msg in st.session_state.chat_history
            if msg["role"] == "user"
        )

        video_titles, video_links = get_yt_video_link(search_query)

        video_refs = []
        st.subheader("🎥 Video References")

        for i in range(min(3, len(video_titles))):
            st.info(f"{video_titles[i]}\n\n🔗 {video_links[i]}")
            video_refs.append((video_titles[i], video_links[i]))

    # SAVE ASSISTANT MESSAGE ONCE
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })
    st.session_state.video_history.append(video_refs)
