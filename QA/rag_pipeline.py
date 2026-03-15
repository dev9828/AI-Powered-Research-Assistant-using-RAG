import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from loaders.all_loaders import custom_loader
from utils.splitter import split_text as custom_text_splitter

# Load API key from environment / .env file
load_dotenv()

# Project root is one level above this file's directory (QA/)
ROOT_DIR = Path(__file__).resolve().parent.parent
VECTORSTORE_DIR = ROOT_DIR / "vectorstore"
DATA_DIR = ROOT_DIR / "data"


class ConversationalRAG:
    def __init__(self):
        # Expect OPENAI_API_KEY (configured in Streamlit / Vercel or local .env)
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment")

        # Use local HuggingFace sentence-transformer embeddings (no external API)
        self.embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatOpenAI(api_key=openai_key, temperature=0.5, model="gpt-4o-mini")
        self.conversation_history = []

        index_path = VECTORSTORE_DIR / "index.faiss"
        if index_path.exists():
            print("🔄 Loading existing FAISS index...")
            self.db = FAISS.load_local(str(VECTORSTORE_DIR), self.embedding, allow_dangerous_deserialization=True)
        else:
            print("⚙️ No index found, creating new one...")
            self._build_index()

        self._create_qa_chain()

    def _create_qa_chain(self):
        """Create a RAG chain using LCEL (LangChain Expression Language)"""
        # Simple RAG prompt template
        template = """You are a helpful assistant that answers questions based on the provided context.
        
Context:
{context}

Question: {question}

Answer:"""
        
        prompt = PromptTemplate.from_template(template)
        
        # Create a RAG chain using LCEL
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})
        
        self.qa_chain = (
            {
                "context": self.retriever | (lambda x: format_docs(x)),
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def _build_index(self):
        documents = custom_loader(str(DATA_DIR))
        split_docs = custom_text_splitter(documents)
        split_docs = [doc for doc in split_docs if doc.page_content.strip()]
        self.db = FAISS.from_documents(split_docs, self.embedding)
        VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
        self.db.save_local(str(VECTORSTORE_DIR))

    def rebuild_index(self):
        print("♻️ Rebuilding FAISS index...")
        self._build_index()
        self.conversation_history = []  # Clear conversation context
        self._create_qa_chain()
        print("✅ Index rebuilt and memory cleared.")

    def ask(self, question: str):
        """Ask a question and get an answer based on the documents"""
        try:
            # Get source documents for reference
            source_docs = self.retriever.invoke(question)
            
            # Get the answer from the chain
            answer = self.qa_chain.invoke(question)
            
            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "answer": answer
            })
            
            return {
                "answer": answer,
                "source_documents": source_docs
            }
        except Exception as e:
            print(f"Error in ask method: {e}")
            return {
                "answer": f"Error processing question: {str(e)}",
                "source_documents": []
            }
