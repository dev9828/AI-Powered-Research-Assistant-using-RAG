# 📚 AI-Powered Research Assistant

An intelligent document analysis system powered by RAG (Retrieval-Augmented Generation), LangChain, and OpenAI.

## ✨ Features

- **📤 Upload Documents** - Support for PDF, DOCX, and TXT files
- **🤖 AI-Powered Q&A** - Ask questions about your documents using GPT-4o-mini
- **🔍 Smart Retrieval** - FAISS-based vector database for accurate document retrieval
- **💬 Conversation History** - Track your questions and answers with source references
- **🎨 Beautiful UI** - Modern, responsive interface built with Streamlit

## 🛠️ Tech Stack

- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Vector Database**: FAISS
- **Framework**: LangChain
- **UI**: Streamlit
- **Language**: Python 3.11

## 📦 Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-Powered-Research-Assistant-using-RAG.git
cd AI-Powered-Research-Assistant-using-RAG
```

2. Create a conda environment:
```bash
conda create -n rag python=3.11
conda activate rag
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

5. Run the app:
```bash
streamlit run frontend/app.py
```

The app will be available at `http://localhost:8501`

## 🚀 Deployment to Streamlit Community Cloud

### Prerequisites
- GitHub account
- Streamlit account (free)
- OpenAI API key

### Step-by-Step Deployment Guide

#### 1️⃣ **Initialize Git Repository Locally**

```bash
cd ~/Diya/AI-Powered-Research-Assistant-using-RAG
git init
git add .
git commit -m "Initial commit: AI Research Assistant with RAG"
```

#### 2️⃣ **Create GitHub Repository**

1. Go to https://github.com/new
2. Repository name: `AI-Powered-Research-Assistant-using-RAG`
3. Description: "AI-Powered Research Assistant using RAG + LangChain + OpenAI"
4. Choose: **Public** (required for Community Cloud free tier)
5. Click **Create repository**

#### 3️⃣ **Add Remote and Push Code**

```bash
git remote add origin https://github.com/yourusername/AI-Powered-Research-Assistant-using-RAG.git
git branch -M main
git push -u origin main
```

**Replace `yourusername` with your actual GitHub username**

#### 4️⃣ **Connect to Streamlit Community Cloud**

1. Go to https://share.streamlit.io
2. Click **Create app** (sign in with GitHub first)
3. Fill in the deployment form:
   - **Repository**: `yourusername/AI-Powered-Research-Assistant-using-RAG`
   - **Branch**: `main`
   - **Main file path**: `frontend/app.py`
4. Click **Deploy**

#### 5️⃣ **Add Secrets to Streamlit Cloud**

Once your app is deployed:

1. Go to your app's deployed page
2. Click **⋯ (three dots)** → **Settings**
3. Click **Secrets** in the left sidebar
4. Add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

5. Click **Save**
6. Your app will automatically redeploy with the secret

### ✅ Verification Checklist

- [ ] .env file is in .gitignore (not pushed to GitHub)
- [ ] All code pushed to GitHub
- [ ] Streamlit Cloud app is connected to your GitHub repo
- [ ] OPENAI_API_KEY is added as a secret in Streamlit Cloud
- [ ] App successfully deployed and accessible

## 🔐 Security Best Practices

- ✅ **Never commit .env files** - Always use .gitignore
- ✅ **Use Streamlit Secrets** - Add API keys in the app settings
- ✅ **Keep repositories public-safe** - Don't commit sensitive data
- ✅ **Rotate API keys** - Regularly update your OpenAI keys
- ✅ **Monitor usage** - Check your OpenAI billing and usage

## 📝 Project Structure

```
AI-Powered-Research-Assistant-using-RAG/
├── frontend/
│   └── app.py                 # Streamlit UI
├── QA/
│   ├── __init__.py
│   └── rag_pipeline.py        # RAG pipeline logic
├── loaders/
│   ├── all_loaders.py         # Document loaders
│   ├── pdf.py
│   ├── doc.py
│   ├── txt.py
│   └── web.py
├── utils/
│   ├── embeddings.py
│   └── splitter.py            # Text splitter
├── vectorstore/
│   ├── faiss_store.py
│   └── index.faiss            # Vector index
├── data/
│   └── uploads/               # User uploaded files
├── requirements.txt           # Python dependencies
├── .env                       # Local secrets (NOT committed)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 💡 Tips for Usage

1. **Upload documents first** - Upload PDF, DOCX, or TXT files
2. **Be specific** - Ask detailed questions for better results
3. **Check sources** - Review the source documents used for answers
4. **Clear history** - Clear chat history to start fresh

## 🐛 Troubleshooting

**Issue**: App says "OPENAI_API_KEY not found"
- **Solution**: Make sure you added the secret in Streamlit Cloud settings

**Issue**: Uploads not working
- **Solution**: Check file format (PDF, DOCX, or TXT) and file size (<200MB)

**Issue**: Slow responses
- **Solution**: This is normal for first queries (embeddings are being generated). Subsequent queries are faster.

## 📞 Support

For issues and questions:
1. Check the GitHub issues
2. Review the code comments
3. Check Streamlit documentation

---

**Built with ❤️ using OpenAI, LangChain, and Streamlit**
