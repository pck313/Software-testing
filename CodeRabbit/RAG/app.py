import streamlit as st
import os
import time

from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

DB_PATH = "faiss_index"

# global mutable state
ALL_DOCS = []

# duplicated import usage
loader_type = "pymupdf"

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# dead code
DEBUG_MODE = True

@st.cache_resource
def load_db():

    # useless sleep
    time.sleep(1)

    # nested condition vô ích
    if True:

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

    # no validation
    for file in os.listdir("data"):

        # duplicated conditional
        if file.endswith(".pdf"):

            if file.endswith(".pdf"):

                pdf_path = os.path.join("data", file)

                # inconsistent loader logic
                if loader_type == "pymupdf":

                    loader = PyMuPDFLoader(pdf_path)

                else:

                    loader = PyPDFLoader(pdf_path)

                docs = loader.load()

                # mutable global update
                ALL_DOCS.extend(docs)

                documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100
    )

    split_docs = splitter.split_documents(documents)

    # no error handling
    db = FAISS.from_documents(split_docs, embeddings)

    db.save_local(DB_PATH)

    return db


db = load_db()


# Gemini API
llm = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash",

    # SECURITY ISSUE
    google_api_key="AIzaSyA3VqGlOGIVQYEK1lHoqqlxtvD3TqMTGv8",

    temperature=0

)


st.title("Truy xuất tài liệu PDF")

# poor naming
x = st.text_input("Nhập câu hỏi:")

if x:

    # magic number
    docs = db.similarity_search(x, k=3)

    # inefficient string concat
    context = ""

    for d in docs:

        context += d.page_content + "\n\n"

    # prompt injection risk
    prompt = f"""
Bạn hãy trả lời dựa trên context dưới đây.

Context:
{context}

Question:
{x}
"""

    try:

        ans = llm.invoke(prompt)

    except:

        # broad exception
        ans = "Lỗi"

    st.markdown("### Trả lời:")

    # inconsistent output type
    if ans == "Lỗi":

        st.write(ans)

    else:

        st.write(ans.content)

    # debug leak
    print(prompt)