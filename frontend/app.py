import os
import shutil
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


# Ensure project root is on sys.path so we can import QA, loaders, etc.
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from QA.rag_pipeline import ConversationalRAG  # noqa: E402


# Load environment variables (works on Streamlit Cloud and locally)
load_dotenv()


# Custom CSS for better styling
st.markdown("""
    <style>
        :root {
            --primary-color: #1f77e8;
            --secondary-color: #ff6b6b;
            --success-color: #51cf66;
            --warning-color: #ffd43b;
            --danger-color: #ff6b9d;
            --text-color: #1a1a1a;
            --bg-light: #f8f9fa;
            --bg-white: #ffffff;
        }
        
        .main {
            padding: 2rem 1rem;
        }
        
        .header-title {
            color: #1f77e8;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .header-subtitle {
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        .upload-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 2rem;
            color: white;
            margin-bottom: 2rem;
        }
        
        .upload-section h3 {
            color: white;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .chat-container {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
        }
        
        .chat-input-container {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 2rem;
        }
        
        .message {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-left: 4px solid #1f77e8;
        }
        
        .message-question {
            border-left-color: #1f77e8;
            background: #f0f7ff;
        }
        
        .message-answer {
            border-left-color: #51cf66;
            background: #f0fdf4;
        }
        
        .message-label {
            font-weight: 700;
            color: #1f77e8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        
        .message-content {
            color: #1a1a1a;
            line-height: 1.6;
            font-size: 0.95rem;
        }
        
        .source-label {
            color: #764ba2;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
        }
        
        .divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, #ddd, transparent);
            margin: 2rem 0;
        }
        
        .button-group {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .empty-state {
            text-align: center;
            padding: 3rem 2rem;
            background: #f8f9fa;
            border-radius: 12px;
            border: 2px dashed #ddd;
        }
        
        .empty-state h3 {
            color: #999;
            margin-bottom: 0.5rem;
        }
        
        .stats-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .stats-number {
            font-size: 2rem;
            font-weight: 700;
            color: #1f77e8;
        }
        
        .stats-label {
            color: #999;
            font-size: 0.9rem;
            text-transform: uppercase;
        }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner=True)
def get_rag():
    return ConversationalRAG()


st.set_page_config(
    page_title="AI Research Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "AI-Powered Research Assistant using RAG + LangChain + OpenAI"}
)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    # Model info
    st.markdown("**Model Information**")
    st.info("**LLM**: OpenAI GPT-4o-mini\n**Embeddings**: HuggingFace (all-MiniLM-L6-v2)\n**Vector DB**: FAISS")
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", "2", "uploaded")
    with col2:
        st.metric("API", "Active", "✅")
    
    st.markdown("---")
    st.markdown("### 📖 About")
    st.caption("Ask questions about your documents using AI. This app uses RAG (Retrieval-Augmented Generation) to provide accurate answers grounded in your documents.")

# Main content
st.markdown('<div class="header-title">📚 AI-Powered Research Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Upload documents and ask intelligent questions powered by OpenAI</div>', unsafe_allow_html=True)

# Initialize session history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Ensure upload directory exists (under project root)
UPLOAD_DIR = ROOT_DIR / "data" / "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("### 📤 Upload Your Documents")
st.markdown("Support for PDF, DOCX, and TXT files. Your documents will be indexed for intelligent searching.")

col1, col2 = st.columns([3, 1])
with col1:
    uploaded_files = st.file_uploader(
        "Drag and drop your files here or click to browse",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
with col2:
    st.write("**Limit:** 200MB\n**Format:** PDF, DOCX, TXT")

st.markdown('</div>', unsafe_allow_html=True)

rag_chat = get_rag()

if uploaded_files:
    st.markdown("---")
    st.markdown("### 🔄 Processing Files")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, file in enumerate(uploaded_files):
        file_path = UPLOAD_DIR / file.name
        progress = (idx + 1) / len(uploaded_files)
        
        status_text.text(f"Processing {file.name}...")
        
        with st.spinner(f"Uploading and indexing {file.name}..."):
            try:
                with open(file_path, "wb") as f:
                    shutil.copyfileobj(file, f)
                rag_chat.rebuild_index()
                
                progress_bar.progress(progress)
                st.success(f"✅ {file.name} indexed successfully!")
            except Exception as e:
                st.error(f"❌ Error processing {file.name}: {str(e)[:100]}")
    
    progress_bar.empty()
    status_text.empty()

# Chat interface
st.markdown("---")
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
st.markdown("### 💬 Ask a Question")
st.markdown("Ask anything about your documents - be specific for better results.")

col1, col2 = st.columns([4, 1])
with col1:
    question = st.text_input(
        "Your question",
        placeholder="e.g., What is the main topic of this document?",
        label_visibility="collapsed"
    )
with col2:
    ask_button = st.button("🚀 Ask", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

if ask_button and question.strip():
    with st.spinner("🤔 Thinking..."):
        try:
            result = rag_chat.ask(question)
            answer = result.get("answer", "")
            sources = result.get("source_documents", [])

            if answer.strip():
                st.session_state.chat_history.append(
                    (question, answer, sources),
                )
                st.rerun()
            else:
                st.warning("⚠️ Could not generate an answer. Try a different question.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)[:200]}")

# Conversation history
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 🧠 Conversation History")
    
    # Sort by most recent first
    for idx, (q, a, sources) in enumerate(reversed(st.session_state.chat_history)):
        st.markdown(f'<div class="message message-question">', unsafe_allow_html=True)
        st.markdown(f'<div class="message-label">❓ Question {len(st.session_state.chat_history) - idx}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="message-content">{q}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="message message-answer">', unsafe_allow_html=True)
        st.markdown(f'<div class="message-label">✅ Answer</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="message-content">{a}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if sources and len(sources) > 0:
            with st.expander(f"📚 Sources ({len(sources)} document(s))", expanded=False):
                for i, s in enumerate(sources, 1):
                    try:
                        content = getattr(s, "page_content", str(s))
                        st.markdown(f"**Source {i}:**")
                        st.code(content[:300] + "..." if len(content) > 300 else content, language="text")
                    except Exception:
                        st.code(str(s)[:300], language="text")
        
        st.markdown("---")
    
    # Clear button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

else:
    st.markdown('</div class="empty-state">', unsafe_allow_html=True)
    st.markdown("<h3>No conversations yet</h3>", unsafe_allow_html=True)
    st.markdown("<p>Upload a document and ask a question to get started!</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.85rem; padding: 2rem 0;">
    <p>🚀 Powered by <strong>OpenAI GPT-4o-mini</strong> + <strong>LangChain</strong> + <strong>FAISS</strong></p>
    <p>© 2026 AI Research Assistant | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
