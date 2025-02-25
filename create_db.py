from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
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

print(JSON_FILES)



def main():
    generate_data_store()
    generate_rag()


def generate_data_store():
    documents = load_documents()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=250)
    splits = text_splitter.split_documents(documents)
    save_to_chroma(splits)


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
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    vectorstore = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k":3})
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

def generate_rag():
    rag_template = """
    You are a Super Smash Brothers Melee frame data expert. You will use the provided context to generate answers to users questions. Refrain from answering with data other than what is provided in the context. Do not answer subjects outside of the context of Super Smash Brothers Melee

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:"""

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, api_key=os.environ['OPENAI_API_KEY'])

    rag_prompt = ChatPromptTemplate.from_template(rag_template)

    question = "Who's jab comes out faster, falcon or marth?"

    rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)
    result = rag_chain.invoke(question)
    retrieved_docs = retriever.invoke(question)
    print(retrieved_docs)
    print(result)


if __name__ == "__main__":
    main()
