# Tabdeal Support Chatbot

A production-oriented Persian customer support chatbot for Tabdeal Exchange built with Django REST Framework, ChromaDB, Retrieval-Augmented Generation (RAG), and GPT-4o-mini.

The chatbot answers user questions using the Tabdeal Help Center knowledge base and includes:

* High-quality RAG pipeline
* Prompt injection protection
* Human handoff detection
* Transaction time estimation
* Message debouncing
* Audit logging
* Source citation
* Simple web-based testing interface

---

# Features

## RAG-based Question Answering

The chatbot retrieves relevant information from the Tabdeal Help Center and generates grounded answers in Persian.

## Prompt Injection Protection

Attempts such as:

* Ignore previous instructions
* Reveal system prompt
* Act as another assistant

are blocked automatically.

## Human Handoff Detection

Conversations are escalated when:

* User requests a human agent
* Missing funds are reported
* Account investigation is required
* Transaction disputes occur

## Time Estimation Tool

When transaction start time is provided, the chatbot estimates remaining processing time using:

Remaining Time =
(Transaction Start Time + Processing Time) − Current Time

## Message Debouncing

Multiple rapid messages are merged and answered as a single request.

## Audit Logging

Every interaction is stored with:

* User message
* Generated answer
* Retrieved sources
* Handoff status
* Timestamp

---

# Project Structure

```text
tabdeal-support-chatbot/
│
├── chatbot/
│   ├── api.py
│   ├── views.py
│   ├── serializers.py
│   ├── models.py
│   ├── handoff.py
│   │
│   ├── rag/
│   │   ├── crawler.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   ├── generator.py
│   │   ├── prompts.py
│   │   └── query_rewriter.py
│   │
│   ├── safety/
│   │   └── guardrails.py
│   │
│   ├── tools/
│   │   └── time_tool.py
│   │
│   └── templates/chatbot/
│       └── index.html
│
├── config/
├── data/
│   └── tabdeal_help.json
│
├── vectorstore/
│   └── chroma/
│
├── manage.py
├── requirements.txt
├── README.md
└── .env.example
```

---

# Technology Stack

## Backend

* Python 3.12
* Django
* Django REST Framework

## AI Components

* OpenRouter
* GPT-4o-mini

## Vector Database

* ChromaDB

## Embedding Model

* sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

## SQL Database

* SQLite

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/DnyaNvB/support-chatbot.git

cd support-chatbot
```

## 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=YOUR_API_KEY

OPENAI_BASE_URL=https://openrouter.ai/api/v1

LLM_MODEL=openai/gpt-4o-mini
```

---

# Build Knowledge Base

## Crawl Help Center

```bash
python chatbot/rag/crawler.py
```

Output:

```text
data/tabdeal_help.json
```

## Generate Embeddings

```bash
python -m chatbot.rag.embeddings
```

Output:

```text
vectorstore/chroma/
```

---

# Database Setup

```bash
python manage.py migrate
```

---

# Run Server

```bash
python manage.py runserver
```

Server:

```text
http://127.0.0.1:8000/
```

---

# Web Interface

Open:

```text
http://127.0.0.1:8000/
```

A Telegram-style testing interface is available for interacting with the chatbot.

---

# API Endpoints

## Chat Endpoint

```http
POST /api/chat/
```

Request:

```json
{
  "message": "چگونه در تبدیل ثبت نام کنم؟"
}
```

Response:

```json
{
  "answer": "...",
  "handoff": false,
  "sources": [
    "https://tabdeal.org/help/guide-to-registration/"
  ]
}
```

---

## Transaction Time Example

Request:

```json
{
  "message": "واریز ارز دیجیتال من کی کامل می‌شود؟",
  "transaction_start_time": "2026-06-21T20:10:00+00:00"
}
```

Response:

```json
{
  "answer": "...",
  "handoff": false,
  "sources": [
    "https://tabdeal.org/help/cryptocurrency-deposit-guide/"
  ]
}
```

---

## Debounced Chat Endpoint

```http
POST /api/chat/debounce/
```

Example:

```json
{
  "session_id": "test1",
  "message": "سلام"
}
```

followed by:

```json
{
  "session_id": "test1",
  "message": "برداشت تومانی چقدر زمان می‌برد؟"
}
```

The chatbot merges rapid messages and produces a single response.

---

# Example cURL Commands

## Registration

```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
-H "Content-Type: application/json" \
-d '{"message":"چگونه در تبدیل ثبت نام کنم؟"}'
```

## Withdrawal

```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
-H "Content-Type: application/json" \
-d '{"message":"برداشت تومانی چقدر زمان می‌برد؟"}'
```

## Human Handoff

```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
-H "Content-Type: application/json" \
-d '{"message":"پولم گم شده و می‌خواهم با پشتیبان انسانی صحبت کنم"}'
```

---

# Implemented Requirements

✅ 3.1 High-Quality RAG

✅ 3.2 Model Selection and Architecture

✅ 3.3 Time Tool

✅ 3.4 Human Handoff

✅ 3.5 Prompt Injection Protection

✅ 4.1 Monitoring Strategy

✅ 4.2 Logging and Traceability

✅ 4.3 Continuous Update Strategy

✅ 5.1 Message Debouncing

✅ 5.2 Frontend Interface

---

# License

This project was developed as part of the AI Engineer Recruitment Project for Tabdeal.
