from flask import Flask, render_template, request
from src.helper import download_embeddings, format_docs
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from src.prompt import *
import os
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = Flask(__name__)

# 1. Configuration
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# 2. Setup Components
embeddings = download_embeddings()
index_name = "medical-chatbot"

# Connect to existing Pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Initialize Gemini
chatModel = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    google_api_key=GEMINI_API_KEY, 
    temperature=0.7
)

# 3. Define the Chain
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# Define retriever
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

# LCEL Chain: Preparation -> Prompt -> LLM -> String Output
rag_chain = (
    {"context": (lambda x: x["input"]) | retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | chatModel
    | StrOutputParser()
)

# 4. Routes
@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print(f"User Message: {msg}")
    
    # Logic fix: invoke returns a string because of StrOutputParser
    response = rag_chain.invoke({"input": msg}) 
    
    print(f"AI Response: {response}")
    return str(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)