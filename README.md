# 📚 StudyPal — RAG Powered AI Study Assistant

StudyPal is a Retrieval-Augmented Generation (RAG) based AI study assistant that helps students learn smarter by generating simple, clear explanations for selected subjects and chapters.
It also provides relevant YouTube video references to support visual learning.

The application is designed to make learning faster, easier, and more personalized using Generative AI.

# ✨ Features

1. 📘 Subject & chapter-based learning

2. 🧠 AI-powered explanations in simple language

3. 🔎 RAG-based content retrieval

4. 🎥 Relevant YouTube video recommendations

5. ⚡ Interactive Streamlit UI

6. ☁️ Deployed on AWS EC2

# 🛠 Tech Stack

1. UI: Streamlit

2. LLM Provider: Groq

3. RAG Framework: LangChain

4. Vector Store: ChromaDB

5. Embeddings: Sentence Transformers

6. Document Processing: Unstructured

7. Cloud Hosting: AWS EC2

8. Language: Python

# 📦 Dependencies

streamlit==1.49.1

python-dotenv==1.1.1

nltk==3.9.1

unstructured==0.18.14

unstructured[pdf]==0.18.14

langchain-community==0.3.29

langchain-huggingface==0.3.1

langchain-chroma==0.2.5

langchain-text-splitters==0.3.11

langchain-groq==0.3.7

transformers==4.56.0

sentence-transformers==5.1.0

youtube-search-python==1.6.6

httpx==0.27.0

# 🧠 How It Works (RAG Flow)

- Student selects subject & chapter

- Study material is processed and split into chunks

- Chunks are embedded and stored in ChromaDB

- Relevant context is retrieved using similarity search

- Groq LLM generates simplified explanations

- Related YouTube videos are fetched for reference

# 🚀 Run Locally

1. Install dependencies

pip install -r requirements.txt


2. Create a .env file

GROQ_API_KEY=your_api_key_here


3. Run the application

streamlit run app.py


4. Open:
👉 http://localhost:8501

# ☁️ Deployment

- Application hosted on AWS EC2

- Streamlit used for serving the UI

- Environment variables managed securely

# 📹 Demo Video:

https://www.youtube.com/watch?v=qgxYdLhtRV8

# 🎯 Why This Project

This project demonstrates:

1. Practical implementation of RAG pipelines

2. Real-world use of LLMs for education

3. Vector search using ChromaDB

4. AI + content retrieval + API integration

5. Cloud deployment experience

# 👨‍💻 Author

Ashish Mittal

Generative AI Developer

# ⭐ If you find this project useful, give it a star!
