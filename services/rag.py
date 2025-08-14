from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.vectorstores.chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
# from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.memory import ConversationBufferMemory
import streamlit as st

from utils.loggers import create_logger


logger = create_logger(__name__)

class RAGService:
    # Cache the expensive initialization so it only runs once per session
    @staticmethod
    @st.cache_resource()
    def _init_resources():
        logger.info("Initializing DirectoryLoader with path 'data/pdfs'")
        loader = DirectoryLoader(path="data/pdfs")
        
        logger.info("Loading documents from directory")
        data = loader.load()
        
        logger.info("Initializing RecursiveCharacterTextSplitter with chunk_size=1000 and chunk_overlap=200")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        logger.info("Splitting documents into chunks")
        chunks = text_splitter.split_documents(data)
        
        logger.info("Initializing OpenAIEmbeddings")
        embeddings = OpenAIEmbeddings(
            api_key=st.secrets.api_keys.openai_api_key,
            model="text-embedding-ada-002"
        )
        
        logger.info("Initializing ChatOpenAI LLM")
        llm = ChatOpenAI(
            api_key=st.secrets.api_keys.openai_api_key,
            model_name='gpt-3.5-turbo'
        )
        
        logger.info("Creating FAISS vectorstore from document chunks")
        vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
        
        logger.info("Initializing ConversationBufferMemory")
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        
        logger.info("Creating ConversationalRetrievalChain from LLM, retriever, and memory")
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        
        logger.info("Resource initialization complete, returning vectorstore and conversation_chain")
        return vectorstore, conversation_chain

    def __init__(self):
        self.vectorstore, self.conversation_chain = RAGService._init_resources()


    def generate_answer(self, query: str):
        
        result = self.conversation_chain({"question": query})
        answer = result["answer"]
        print(answer)
        
        return answer
    
    
    def retrieve_relevant_context(self, query):
        # vector_store = load_vector_store()
        docs = self.vectorstore.similarity_search(query)
        return "\n".join([doc.page_content for doc in docs])


    # def generate_gpt_response(self, prompt):
    #     # Use OpenAI API or any GPT model to generate the response
    #     import openai
    #     openai.api_key = st.secrets.api_keys.openai_api_key
    #     response = openai.Completion.create(
    #         engine="text-davinci-003",
    #         prompt=prompt,
    #         max_tokens=150
    #     )
    #     return response.choices[0].text.strip()


rag_service = RAGService()
