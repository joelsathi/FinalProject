from langchain.document_loaders import TextLoader  # for textfiles
from langchain.text_splitter import CharacterTextSplitter  # text splitter
from langchain.embeddings import HuggingFaceEmbeddings  # for using HugginFace models
from langchain.chains.question_answering import load_qa_chain
from pypdf import PdfReader
from io import BytesIO
from typing import Any, Dict, List
import re


from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    "C:\\Users\\Sanu\\Desktop\\FinalProject\\BackEnd\\VectorDB_chat\\Data\\Bank of Mora.pdf"
)
documents = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=400,
    chunk_overlap=20,
    length_function=len,
    separators=["\n\n"]
    # TODO: Add seperator regex
)

docs = text_splitter.split_documents(documents)
# print(docs[0].page_content)
# print(len(docs))

# # Embeddings

from langchain.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# from langchain.embeddings import HuggingFaceEmbeddings
# embeddings = HuggingFaceEmbeddings()

from langchain.vectorstores import Chroma

db = Chroma.from_documents(docs, embeddings, persist_directory="../../db")

# # Testing
# query = "List out some transaction accounts."
# docs = db.similarity_search(query)

# print(len(docs))
# print(docs)
# print(len(docs[0].page_content))
