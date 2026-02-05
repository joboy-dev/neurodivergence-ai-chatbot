import os
from typing import ClassVar, List
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
import streamlit as st

from utils.loggers import create_logger

logger = create_logger(__name__)

# Custom QA prompt for symptom-to-disorder identification
QA_SYSTEM_PROMPT = """You are a supportive assistant helping parents and caregivers understand neurodevelopmental conditions in children based on symptoms they describe.

Your role is to:
1. Analyze the symptoms the user provides based on the retrieved context from medical and educational literature.
2. Suggest possible conditions that may align with those symptoms (e.g., ADHD, autism, dyslexia) - but ONLY based on information found in the provided context.
3. Structure your response clearly: summarize the symptoms mentioned, discuss possible conditions from the literature, and recommend next steps.
4. Always emphasize that you are providing informational support only - you cannot diagnose. Recommend that they consult a qualified healthcare professional (pediatrician, psychologist, or specialist) for proper evaluation.
5. Be empathetic, non-judgmental, and avoid making definitive diagnostic claims.
6. If the retrieved context does not contain relevant information about the symptoms described, say so and suggest they seek professional guidance.

Use only the following context from our knowledge base to inform your response. Do not make up information:"""

CONTEXTUALIZE_Q_PROMPT = """Given the conversation history and the latest user question, rephrase the question to be a standalone question that captures all relevant context for retrieval. If the chat history is empty or not relevant, return the question unchanged."""

class RAGService:
    @staticmethod
    @st.cache_resource()
    def _init_resources():
        # Use absolute path for reliable document loading
        data_path = os.path.join(os.path.dirname(__file__), "..", "data")
        logger.info(f"Initializing DirectoryLoader with path '{data_path}'")
        loader = DirectoryLoader(path=data_path, glob="**/*.pdf", loader_cls=PyPDFLoader)

        logger.info("Loading documents from directory")
        data = loader.load()

        logger.info("Initializing RecursiveCharacterTextSplitter with chunk_size=1000 and chunk_overlap=200")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        logger.info("Splitting documents into chunks")
        chunks = text_splitter.split_documents(data)
        if not data:
            logger.warning("No documents loaded from 'data'.")
        if not chunks:
            logger.warning("No chunks produced from documents; initializing an empty vector store placeholder.")

        logger.info("Initializing OpenAIEmbeddings")
        embeddings = OpenAIEmbeddings(
            api_key=st.secrets.api_keys.openai_api_key,
            model="text-embedding-3-small"
        )

        logger.info("Initializing ChatOpenAI LLM")
        llm = ChatOpenAI(
            api_key=st.secrets.api_keys.openai_api_key,
            model_name="gpt-4o-mini"
        )

        logger.info("Creating FAISS vectorstore from document chunks")
        if chunks:
            vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
        else:
            vectorstore = FAISS.from_texts([""], embedding=embeddings)

        # Retriever with increased k for symptom matching (retrieve more context)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

        logger.info("Creating contextualize question prompt")
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", CONTEXTUALIZE_Q_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        logger.info("Creating history-aware retriever")
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

        logger.info("Creating QA prompt and document chain")
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", QA_SYSTEM_PROMPT + "\n\n{context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        logger.info("Creating retrieval chain")
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        logger.info("Resource initialization complete")
        return vectorstore, rag_chain

    def __init__(self):
        self.vectorstore, self.rag_chain = RAGService._init_resources()

    def generate_answer(self, query: str, chat_history=None):
        """
        Generate an answer using RAG with per-chat conversation history.
        chat_history: list of (role, content) tuples from DB, e.g. [("user", "..."), ("assistant", "...")]
        """
        if chat_history is None:
            chat_history = []

        # Convert DB messages to LangChain format
        langchain_history = []
        for role, content in chat_history:
            if role == "user":
                langchain_history.append(HumanMessage(content=content))
            else:
                langchain_history.append(AIMessage(content=content))

        result = self.rag_chain.invoke({
            "input": query,
            "chat_history": langchain_history,
        })
        answer = result["answer"]
        return answer

    def retrieve_relevant_context(self, query):
        docs = self.vectorstore.similarity_search(query, k=6)
        return "\n".join([doc.page_content for doc in docs])


rag_service = RAGService()
