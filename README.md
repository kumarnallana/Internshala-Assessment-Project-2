# AI-Powered Export Lead Generation & Outreach Automation

This project is a complete end-to-end web application built for the Internshala assessment. It automates the process of discovering international buyers, classifying them using Artificial Intelligence, and dispatching personalized outreach campaigns with PDF attachments.

## 🚀 Features

- **Live Lead Discovery:** Real-time web scraping engine that queries search engines to find live B2B and B2C leads based on your product keywords (e.g., "Singing Bowls").
- **AI-Powered Classification:** Integrates with OpenAI's ChatGPT (`gpt-4o-mini`) to automatically classify extracted emails into `BUSINESS` or `INDIVIDUAL` segments with high accuracy.
- **Automated Email Dispatch:** Seamlessly connects to Gmail SMTP to dispatch personalized email campaigns.
- **Analytics & Reporting:** Tracks delivery metrics and generates a downloadable audit CSV (`sent_log.csv`).
- **Modern UI/UX:** A stunning, responsive, glassmorphism-inspired dashboard that provides real-time feedback on leads.

## 🛠️ Technology Stack

- **Backend:** FastAPI, Python 3
- **Frontend:** Jinja2 Templates, HTML5, CSS3, JavaScript
- **AI Integration:** OpenAI API (`gpt-4o-mini`)
- **Web Scraping:** BeautifulSoup4, Requests
- **Email:** Python `smtplib`, `email.mime`

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Internshala-Assessment-Project-2
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Open the `.env` file and set up your credentials:
   ```env
   GMAIL_EMAIL=your_email@gmail.com
   GMAIL_APP_PASSWORD=your_app_password
   OPENAI_API_KEY=sk-proj-...
   ```

## 🏃 How to Run

Start the FastAPI local server using Uvicorn:

```bash
python run.py
```

Then, open your web browser and navigate to:
**http://127.0.0.1:8000**

## 💡 Usage Workflow

1. **Discover Leads:** Go to the Dashboard and click "Discover Leads". Enter your product keyword and run the live web scraper.
2. **Classify with AI:** Click "Classify with AI" to send the harvested leads to ChatGPT for automatic segmentation.
3. **Dispatch Campaign:** Click "Dispatch Campaign", select your target audience, and launch the outreach. (Set `DRY_RUN=true` in `.env` to test without sending real emails).
4. **Download Report:** View the delivery log and download the Audit CSV report.