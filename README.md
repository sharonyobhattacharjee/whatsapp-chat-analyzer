# WhatsApp Chat Analyzer

A full-stack **WhatsApp Chat Analytics Dashboard** that transforms exported WhatsApp chat `.txt` files into interactive insights about conversations, activity patterns, participants, emojis, links, media, and messaging behavior.

**Live Demo:** https://whatsapp-chat-analyzer-gilt.vercel.app  


---

## ✨ Features

### 📊 Chat Statistics
Analyze your entire conversation or an individual participant and get:

- Total messages
- Total words
- Media messages
- Links shared
- Participant count

### 📈 Conversation Timeline

Visualize messaging activity over time with:

- Monthly message timeline
- Daily message timeline
- Message frequency trends

### 👥 Participant Analysis

For group conversations:

- Most active participants
- Messages sent by each participant
- Percentage contribution of each participant
- Individual participant analysis

### 🗓️ Activity Analysis

Understand when conversations are most active through:

- Most active days of the week
- Weekly activity distribution
- Hour-by-hour activity heatmap

### ☁️ Word Cloud

Generate a visual representation of the most frequently used words in the conversation.

### 😀 Emoji Analysis

Analyze emoji usage with:

- Most frequently used emojis
- Emoji frequency table
- Emoji distribution chart

### 👤 Individual User Analysis

Select any participant and generate analytics specifically for that person.

---

## 🖥️ Dashboard

The application provides an interactive web dashboard where users can upload a WhatsApp exported `.txt` file and instantly generate analytics.

**Workflow:**

```text
WhatsApp Chat Export
        │
        ▼
   Upload .txt file
        │
        ▼
   Flask API
        │
        ▼
 Chat Preprocessing
        │
        ▼
 Analytics Engine
        │
        ▼
 Interactive Dashboard
```

---

## 🏗️ Architecture

```text
┌───────────────────────────────┐
│       WhatsApp Export         │
│          .txt file            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Web Dashboard          │
│      HTML + CSS + JS          │
│          Chart.js             │
└───────────────┬───────────────┘
                │
                │ POST /api/analyze
                ▼
┌───────────────────────────────┐
│          Flask API            │
│         api/index.py          │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Chat Preprocessor        │
│       preprocessor.py         │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Analytics Engine        │
│          helper.py            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Analysis Results       │
│  Stats • Charts • Heatmap     │
│  Word Cloud • Emojis          │
└───────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js

### Backend

- Python
- Flask
- REST API

### Data Processing

- Pandas
- Python Regex
- Collections
- URLExtract

### Visualization

- Chart.js
- WordCloud
- Matplotlib
- Seaborn

### Deployment

- Vercel
- GitHub

---

## 📁 Project Structure

```text
whatsapp-chat-analyzer/
│
├── api/
│   └── index.py
│
├── templates/
│   └── index.html
│
├── app.py
├── helper.py
├── preprocessor.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `api/index.py`

Flask API used by the Vercel deployment.

Handles:

- Dashboard rendering
- Health check
- Chat file upload
- Chat analysis
- JSON response generation

### `preprocessor.py`

Responsible for converting raw WhatsApp exported text into structured Pandas data.

It extracts:

- Date
- Time
- User
- Message
- Year
- Month
- Day
- Day name
- Hour
- Minute
- Time period

### `helper.py`

Contains the analytics layer responsible for generating:

- Chat statistics
- Word counts
- Link counts
- Media counts
- Monthly timelines
- Daily timelines
- Activity analysis
- User rankings
- Word clouds
- Emoji statistics
- Heatmap data

### `templates/index.html`

Contains the interactive dashboard UI and visualization logic.

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/sharonyobhattacharjee/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the Flask application

```bash
python -m flask --app api/index.py run
```

### 5. Open the dashboard

Visit:

```text
http://127.0.0.1:5000
```

Upload your WhatsApp exported `.txt` file and start analyzing.

---

## 📱 How to Export a WhatsApp Chat

From WhatsApp, export the conversation as a **text-only chat**.

For the best results:

- Export **without media**
- Upload the resulting `.txt` file
- Select **Overall** or a specific participant
- Click **Analyze**

The application processes the exported chat and generates the dashboard.

---

## 🔌 API

### Health Check

```http
GET /api/health
```

Example response:

```json
{
  "status": "success",
  "message": "WhatsApp Chat Analyzer API is running on Vercel"
}
```

### Analyze Chat

```http
POST /api/analyze
```

Form data:

```text
chat = WhatsApp exported .txt file
user = Overall
```

The endpoint returns structured JSON containing:

```text
statistics
monthly_timeline
daily_timeline
busy_days
heatmap
busy_users
user_percent
wordcloud
emoji
```

---

## 🔐 Privacy

The analyzer is designed around **local processing of uploaded chat data during analysis**.

Your WhatsApp conversations should be treated as sensitive information. Do not upload chats containing information you are not comfortable processing through a third-party hosted service.

For highly sensitive conversations, running the project locally is recommended.

---

## ⚠️ Current Limitations

The application currently depends on the format of WhatsApp's exported `.txt` chat data.

Very large chat exports may also
