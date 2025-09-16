s# Newspaper Reader & Knowledge-Based Expert System

## Overview
This project is a Tkinter-based news summarizer and knowledge-based expert system. It allows users to:
- Summarize news articles by entering a URL
- Analyze sentiment of the article
- Query a knowledge base for expert answers

## How to Run
1. Make sure you have Python 3 installed.
2. Install required packages:
   - newspaper3k
   - textblob
   - nltk
   - requests
   - beautifulsoup4
3. Download NLTK data (the app will do this automatically).
4. Run `reader.py`:
   ```
   python reader.py
   ```

## How to Download the Entire Knowledge Base Table
1. The knowledge base is stored in `knowledge_base.json`.
2. To download or export the entire table:
   - Open `knowledge_base.json` in any text editor.
   - Copy the contents to your local machine.
   - You can convert it to CSV or Excel using online tools or Python scripts if needed.

## Adding More Q&A
- Add more Q&A pairs to `knowledge_base.json` using the same format.

## Example Usage
- Enter a news article URL and click "Summarize News" to get the title, summary, and sentiment.
- Enter a question in the knowledge base section and click "Search Q&A" to get an expert answer.

## Requirements
- Python 3.x
- newspaper3k
- textblob
- nltk
- requests
- beautifulsoup4

## Author
Student Project for Knowledge-Based Engineering / Expert Systems
