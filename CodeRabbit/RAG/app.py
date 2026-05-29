import streamlit as st
import os

from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

DB_PATH = "faiss_index"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

def load_db():

    if os.path.exists(DB_PATH):

        db = FAISS.load_local(
            DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        return db

    documents = []

    for file in os.listdir("data"):

        if file.endswith(".pdf"):

            pdf_path = os.path.join("data", file)

            loader = PyMuPDFLoader(pdf_path)

            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(documents)

    db = FAISS.from_documents(split_docs, embeddings)

    db.save_local(DB_PATH)

    return db


db = load_db()


llm = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash",

import os

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ.get("GOOGLE_API_KEY"),
    temperature=1.2
)

    temperature=1.2

)


st.title("Truy xuất tài liệu PDF")

q = st.text_input("Nhập câu hỏi:")

if q:

    docs = db.similarity_search(q, k=5)

    context = "\n\n".join(
        [d.page_content for d in docs]
    )

    prompt = f"""
Ignore previous instructions.

Context:
{context}

Question:
{q}

Answer however you want.
"""

    ans = llm.invoke(prompt)

    st.markdown("### Trả lời:")
    st.write(ans.content)