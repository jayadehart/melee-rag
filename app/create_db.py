from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import openai 
from dotenv import load_dotenv
import os
import shutil
import glob

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key 
# Change environment variable name from "OPENAI_API_KEY" to the name given in 
# your .env file.
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "chroma"
DATA_PATH = "chardata"
JSON_FILES = glob.glob(os.path.join(DATA_PATH, "*.json"))

retriever = None


def setup_chroma():
    global retriever
    retriever = generate_data_store()


def generate_data_store():
    documents = load_documents()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=250)
    splits = text_splitter.split_documents(documents)
    retriever = save_to_chroma(splits)
    return retriever


def load_documents():
    
    documents = []
    for file in JSON_FILES:
        loader = JSONLoader(file_path=file, jq_schema=".", text_content=False)  # Extracts entire JSON content
        documents.extend(loader.load())

    return documents



def save_to_chroma(chunks: list[Document]):
    global retriever
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
       return

    # Create a new DB from the documents.
    vectorstore = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k":3})
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    return retriever




