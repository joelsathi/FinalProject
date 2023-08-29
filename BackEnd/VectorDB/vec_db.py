from langchain.document_loaders import TextLoader  #for textfiles
from langchain.text_splitter import CharacterTextSplitter #text splitter
from langchain.embeddings import HuggingFaceEmbeddings #for using HugginFace models
from langchain.chains.question_answering import load_qa_chain
from pypdf import PdfReader
from io import BytesIO
from typing import Any, Dict, List
import re

def parse_pdf(file: BytesIO) -> List[str]:
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        # Merge hyphenated words
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        # Fix newlines in the middle of sentences
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        # Remove multiple newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)
        output.append(text)
    return output

from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\BackEnd\\VectorDB\\Data\\bank_domain.pdf")
documents = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 200,
    chunk_overlap  = 20,
    length_function = len,
    is_separator_regex = False,
    #TODO: Add seperator regex
)
docs = text_splitter.split_documents(documents)

# # Embeddings

from langchain.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# from langchain.embeddings import HuggingFaceEmbeddings
# embeddings = HuggingFaceEmbeddings()

from langchain.vectorstores import Chroma
db = Chroma.from_documents(docs, embeddings, persist_directory="../db")

# Testing
query = "List out some transaction accounts."
docs = db.similarity_search(query)

print(len(docs))
print(docs)

