# chatbot.py
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Replace this import
# from langchain.llms import GoogleGenerativeAI
# With this import
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema.document import Document
from dotenv import load_dotenv

load_dotenv()

class StockChatbot:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize Vector DB
        self.db_directory = "chroma_db"
        if os.path.exists(self.db_directory):
            self.vector_db = Chroma(
                persist_directory=self.db_directory,
                embedding_function=self.embedding_model
            )
        else:
            self.vector_db = None
            
        # Initialize LLM - updated to use ChatGoogleGenerativeAI
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1
        )
        
        # Text splitter for document chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        
        # Create QA chain
        self.qa_template = """
        You are a helpful AI assistant who specializes in financial news analysis.
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say you don't know, don't try to make up an answer.
        Be concise and to-the-point, providing factual information.
        
        Context: {context}
        
        Question: {question}
        
        Answer:
        """
        
        self.qa_prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=["context", "question"]
        )
        
        if self.vector_db:
            self.qa_chain = self._create_qa_chain()
            
    def _create_qa_chain(self):
        """Create retrieval QA chain"""
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": self.qa_prompt}
        )
            
    def update_knowledge_base(self, articles):
        """Update the vector database with new articles"""
        documents = []
        
        for article in articles:
            text = f"Title: {article['title']}\n"
            text += f"Source: {article['source']['name']}\n"
            text += f"Published: {article['publishedAt']}\n"
            text += f"Sentiment: {article.get('sentiment', {}).get('label', 'N/A')}\n\n"
            text += article.get('content', 'No content available.')
            
            metadata = {
                'title': article['title'],
                'source': article['source']['name'],
                'url': article['url'],
                'published_at': article['publishedAt'],
                'sentiment': article.get('sentiment', {}).get('label', 'neutral')
            }
            
            documents.append(Document(page_content=text, metadata=metadata))
        
        # Split documents into chunks
        splits = self.text_splitter.split_documents(documents)
        
        # Update vector store
        if not self.vector_db:
            self.vector_db = Chroma.from_documents(
                documents=splits,
                embedding=self.embedding_model,
                persist_directory=self.db_directory
            )
        else:
            self.vector_db.add_documents(splits)
            self.vector_db.persist()
        
        # Recreate QA chain
        self.qa_chain = self._create_qa_chain()
            
    def ask(self, question):
        """Ask a question to the chatbot"""
        if not self.vector_db:
            return "I don't have any stock information loaded yet. Please update the knowledge base first."
        
        try:
            result = self.qa_chain.invoke({"query": question})
            return result['result']
        except Exception as e:
            return f"I encountered an error while processing your question: {str(e)}"