from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
from dotenv import load_dotenv
import os
import json

CHROMA_PATH = "chroma"

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']



def query_rag(question):
    rag_template = """
    You are a Super Smash Brothers Melee frame data expert. You will use the provided context to generate answers to users questions. Refrain from answering with data other than what is provided in the context. Do not answer subjects outside of the context of Super Smash Brothers Melee

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:"""

    ## reinitialize the vector store and retriever here by using the chroma store url 
    embedding_function = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    retriever = vectorstore.as_retriever(search_kwargs={"k":3})



    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, api_key=os.environ['OPENAI_API_KEY'])

    rag_prompt = ChatPromptTemplate.from_template(rag_template)


    rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)
    
    retrieved_docs = retriever.invoke(question)
    result = rag_chain.invoke(question)

    return {"answer": result, "sources": retrieved_docs}
    



    

    