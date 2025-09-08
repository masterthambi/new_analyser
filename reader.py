
import tkinter as tk
import nltk
from textblob import TextBlob
from newspaper import Article
import requests
from bs4 import BeautifulSoup

try:
	nltk.data.find('tokenizers/punkt')
except LookupError:
	nltk.download('punkt')
try:
	nltk.data.find('tokenizers/punkt_tab')
except LookupError:
	nltk.download('punkt_tab')
nltk.download('punkt')


def fetch_article():
	url = url_entry.get()
	if not url.strip():
		result_title.config(text="Please enter a valid URL.")
		result_summary.config(text="")
		result_sentiment.config(text="")
		return
	try:
		article = Article(url)
		article.download()
		article.parse()
		if article.text and len(article.text.strip()) > 0:
			article.nlp()
			analysis = TextBlob(article.text)
			title = article.title if article.title else "No Title Found"
			summary = article.summary if article.summary else "No Summary Found"
			sentiment = f"Polarity: {analysis.polarity:.2f}, Subjectivity: {analysis.subjectivity:.2f} | Sentiment: {'Positive' if analysis.polarity > 0 else 'Negative' if analysis.polarity < 0 else 'Neutral'}"
			result_title.config(text=title)
			result_summary.config(text=summary)
			result_sentiment.config(text=sentiment)
			return
		# Fallback: Use BeautifulSoup for BBC and similar sites
		response = requests.get(url, timeout=10)
		if response.status_code != 200:
			raise Exception(f"HTTP error: {response.status_code}")
		soup = BeautifulSoup(response.text, 'html.parser')
		# BBC article main text is often in <article> or <div> with role="main"
		main = soup.find('article') or soup.find('div', {'role': 'main'})
		if not main:
			main = soup
		paragraphs = main.find_all('p')
		text = '\n'.join([p.get_text() for p in paragraphs if p.get_text().strip()])
		if not text or len(text.strip()) == 0:
			raise Exception("Could not extract article text. The site may block scraping or the URL is not a news article.")
		analysis = TextBlob(text)
		# Try to get title from <title> or <h1>
		title = soup.title.string if soup.title else "No Title Found"
		h1 = soup.find('h1')
		if h1 and h1.get_text().strip():
			title = h1.get_text().strip()
		# Simple summary: first 2-3 sentences
		summary = ' '.join(text.split('.')[:3]) + '.'
		sentiment = f"Polarity: {analysis.polarity:.2f}, Subjectivity: {analysis.subjectivity:.2f} | Sentiment: {'Positive' if analysis.polarity > 0 else 'Negative' if analysis.polarity < 0 else 'Neutral'}"
		result_title.config(text=title)
		result_summary.config(text=summary)
		result_sentiment.config(text=sentiment)
	except Exception as e:
		result_title.config(text="Error fetching article.")
		result_summary.config(text=f"Details: {str(e)}\nTry a different news URL or check your internet connection.")
		result_sentiment.config(text="")

root = tk.Tk()
root.title("News Article Reader")
root.geometry('1200x600')


# --- News Summarizer UI ---
tk.Label(root, text="Enter News Article URL:", font=("Helvetica", 16, "bold"), fg="#333").pack(pady=20)
url_entry = tk.Entry(root, width=90, font=("Helvetica", 14))
url_entry.pack(pady=5)
fetch_btn = tk.Button(root, text="Summarize News", font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", command=fetch_article)
fetch_btn.pack(pady=15)

result_frame = tk.Frame(root, bg="#f9f9f9")
result_frame.pack(fill="both", expand=True, padx=30, pady=20)

result_title = tk.Label(result_frame, text="", font=("Helvetica", 18, "bold"), wraplength=1100, bg="#fff", fg="#222")
result_title.pack(fill="x", pady=(0,10))

result_summary = tk.Label(result_frame, text="", font=("Helvetica", 14), wraplength=1100, justify="left", bg="#f6f6f6", fg="#444")
result_summary.pack(fill="x", pady=(0,10))

result_sentiment = tk.Label(result_frame, text="", font=("Helvetica", 13, "italic"), wraplength=1100, bg="#e3f2fd", fg="#1565c0")
result_sentiment.pack(fill="x", pady=(0,10))

root.mainloop()

