
# DeepStock AI – Real-Time Financial News Sentiment and Query System

**DeepStock AI** is an AI-powered web application that provides real-time sentiment analysis of stock market news and enables intelligent query responses based on the latest financial information. It combines automated news aggregation, sentiment classification using a fine-tuned finBERT model, and a context-aware query system built on LangChain, ChromaDB, and Gemini LLM. The project features a clean HTML/CSS frontend served by a FastAPI backend.

---

## 🔧 Features

- **Real-Time News Retrieval**  
  Fetches up-to-date news articles related to any stock ticker using NewsAPI and Selenium scraping from sources like Yahoo Finance and MarketWatch.

- **Sentiment Analysis**  
  Uses finBERT to classify each news article as positive, neutral, or negative, helping users gauge market sentiment.

- **Context-Aware Query System**  
  Supports natural language queries based on the retrieved news using LangChain, ChromaDB, and Gemini LLM.

- **Interactive Web Interface**  
  Built with FastAPI and HTML/CSS, allowing users to input stock tickers, view sentiment summaries, and ask finance-related questions.

- **Sentiment Visualization**  
  Visual output of sentiment distribution using Matplotlib.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI  
- **Frontend**: HTML, CSS  
- **NLP**: finBERT (financial sentiment analysis)  
- **News Aggregation**: NewsAPI, Selenium  
- **Query Engine**: LangChain, ChromaDB, Gemini LLM  
- **Visualization**: Matplotlib

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/DeepStockAI.git
cd DeepStockAI
```

### 2. Install Dependencies
Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

Install required packages:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
uvicorn backend:app
```

Then open your browser at:  
**http://localhost:8000**

---

## 📁 Project Structure

```
DeepStockAI/
├── backend.py                 # Main FastAPI application
├── chatbot.py                 # Handles Gemini + LangChain logic
├── news_fetcher.py            # NewsAPI and Selenium logic
├── sentiment_analyzer.py      # finBERT sentiment classification
├── README.md                  # Project documentation
├── static/
│   └── style.css              # CSS styles
├── templates/
│   └── index.html             # HTML frontend
├── requirements.txt
└── README.md
```

---

## 💡 Example Use Cases

- Monitor real-time sentiment for stocks like `AAPL`, `GOOGL`, `TSLA`  
- Ask:  
  - “What’s the latest sentiment on Tesla?”  
  - “Why is Apple stock in the news today?”

---

## 📌 Future Enhancements

- Add user authentication and watchlists  
- Compare sentiment trends across multiple tickers  
- Dockerize the app and deploy on cloud platforms

---

## 🧠 Credits

- [finBERT – Hugging Face](https://huggingface.co/yiyanghkust/finbert-tone)  
- [LangChain](https://www.langchain.com/)  
- [ChromaDB](https://www.trychroma.com/)  
- [Google Gemini API](https://ai.google.dev/)  
- [NewsAPI](https://newsapi.org/)

---

