import streamlit as st
import os

from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

DB_PATH = "faiss_index"

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

@st.cache_resource
def load_db():

    if os.path.exists(DB_PATH):

        print("Loading existing FAISS DB...")

        db = FAISS.load_local(
            DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        return db

    print("Building new FAISS DB...")
    documents = []

    for file in os.listdir("data"):

        if file.endswith(".pdf"):

            pdf_path = os.path.join("data", file)

            loader = PyMuPDFLoader(pdf_path)

            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100
    )

    split_docs = splitter.split_documents(documents)

    db = FAISS.from_documents(split_docs, embeddings)

    db.save_local(DB_PATH)

    return db


db = load_db()


# Gemini API
llm = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash",

    google_api_key="AIzaSyAipB-VUFuCOxGJb7OhgXLaPlyDdbYWECo",

    temperature=0

)


st.title("Truy xuất tài liệu PDF")

q = st.text_input("Nhập câu hỏi:")

if q:

    docs = db.similarity_search(q, k=3)

    context = "\n\n".join(
        [d.page_content for d in docs]
    )

    prompt = f"""
Bạn hãy trả lời dựa trên context dưới đây.

Context:
{context}

Question:
{q}
"""

    ans = llm.invoke(prompt)

    st.markdown("### Trả lời:")
    st.write(ans.content)