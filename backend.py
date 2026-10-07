from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from news_fetcher import NewsFetcher
from sentiment_analyzer import SentimentAnalyzer
from chatbot import StockChatbot
import uvicorn
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

news_fetcher = NewsFetcher()
sentiment_analyzer = SentimentAnalyzer()
chatbot = StockChatbot()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/news", response_class=HTMLResponse)
def news_get(request: Request, ticker: Optional[str] = None):
    articles = []
    sentiment_summary = None
    if ticker:
        articles = news_fetcher.fetch_stock_news(ticker)
        if articles:
            articles = sentiment_analyzer.analyze_articles(articles)
            chatbot.update_knowledge_base(articles)
            sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
            for article in articles:
                if 'sentiment' in article:
                    sentiment_counts[article['sentiment']['label']] += 1
            total = sum(sentiment_counts.values())
            sentiment_summary = {k: f"{v} ({v/total*100:.1f}%)" if total else "0 (0%)" for k, v in sentiment_counts.items()}
    return templates.TemplateResponse("news.html", {"request": request, "ticker": ticker, "articles": articles, "sentiment_summary": sentiment_summary})

@app.post("/news", response_class=HTMLResponse)
def news_post(request: Request, ticker: str = Form(...)):
    return RedirectResponse(url=f"/news?ticker={ticker}", status_code=303)

@app.get("/chatbot", response_class=HTMLResponse)
def chatbot_get(request: Request, ticker: Optional[str] = None, chat_history: Optional[str] = None):
    import ast
    try:
        chat_history_list = ast.literal_eval(chat_history) if chat_history else []
    except Exception:
        chat_history_list = []
    return templates.TemplateResponse("chatbot.html", {"request": request, "ticker": ticker, "chat_history": chat_history_list})

@app.post("/chatbot", response_class=HTMLResponse)
def chatbot_post(request: Request, ticker: str = Form(""), user_query: str = Form(...), chat_history: str = Form("")):
    import ast
    try:
        chat_history_list = ast.literal_eval(chat_history) if chat_history else []
    except Exception:
        chat_history_list = []
    chat_history_list.append({"role": "user", "content": user_query})
    response = chatbot.ask(user_query)
    chat_history_list.append({"role": "assistant", "content": response})
    return templates.TemplateResponse("chatbot.html", {"request": request, "ticker": ticker, "chat_history": chat_history_list})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 