# Tanyain — Multi-Tenant AI Customer Service & Automated Ordering SaaS 🚀

**Tanyain** is a lightweight, multi-tenant AI-powered SaaS platform engineered to help SMEs and educational institutions automate customer support and stream order processing. Powered by a custom **TF-IDF (Term Frequency-Inverse Document Frequency)** natural language processing engine and cosine similarity algorithms, Tanyain delivers instant, contextual FAQ responses with high accuracy without the overhead of heavy LLM infrastructure.

The platform features a multi-tenant architecture enabling seamless merchant onboarding, dynamic sub-path route slugs, automated order processing webhooks, and single-source-of-truth (SSOT) database syncing.

---

## 📺 Live System Demonstrations

- 🎥 **[Full SaaS & AI Workflow Demo](https://youtu.be/n5JUtc0aTcA)**: Demonstrates multi-tenant merchant onboarding, bulk CSV dataset training, analytics dashboard, and real-time response matching.
- 🎥 **[24/7 CS & Order Automation Demo](https://youtu.be/iGgr0OmKriQ)**: Simulates end-to-end automated customer inquiries and frictionless order submission directly within the chat widget.

---

## 🌟 Key Features

- **Multi-Tenant Architecture**: Dynamic URL slug routing per business tenant with Super Admin approval mechanisms.
- **Lightweight AI Engine (TF-IDF)**: Efficient response matching using `scikit-learn` vectorizers and threshold-based fallbacks for accurate intent classification.
- **Automated Order Capture**: In-chat order workflow that validates cart payloads and pushes data to backend HTTP endpoints.
- **SSOT Integration Ready**: Built-in `/submit_order` webhook endpoint prepared for automation tools (e.g., Make.com) to synchronize data into Airtable/Databases.
- **Analytics & Merchant Dashboard**: Real-time operational metrics showing query volume, top asked questions, and resolved vs. unresolved inquiry ratios.
- **Bulk CSV Data Management**: Seamless bulk import/export for tenant FAQ datasets and automatic store QR code generation.
- **Production-Grade Security**: 12-Factor app architecture isolating environment variables (`os.environ`), hashed authentication (`Werkzeug`), and zero hardcoded credentials.

---

## 📐 System Architecture & Workflow

```mermaid
graph TD
    A[End User / Customer] -->|Interacts via Chat Widget| B(Flask Backend Service)
    B -->|Extract TF-IDF Vectors| C[Scikit-Learn NLP Engine]
    C -->|Calculate Cosine Similarity| B
    B -->|Render Contextual Response| A
    
    A -->|Triggers Automated Order| D[Submit Order Endpoint]
    D -->|Secure HTTP POST Webhook| E[Make.com Automation]
    E -->|Sync Transaction Data| F[(Airtable / SSOT Database)]

🛠️ Tech Stack
-Backend: Python (Flask)
-Database & ORM: SQLite, Flask-SQLAlchemy (with SQLAlchemy Enum Role Management)
-Machine Learning: Scikit-learn (TfidfVectorizer, cosine_similarity)
-Frontend: React.js, Tailwind CSS, HTML5, Vanilla JS (Fetch API)
-Security & Utils: Werkzeug (Password Hashing), Requests, PyQRCode

🚀 Quickstart & Local Installation
Prerequisites
Python 3.8+ installed on your system.

1. Clone Repository
git clone [https://github.com/Gayoyo/Tanyain-Customer-Service.git](https://github.com/Gayoyo/Tanyain-Customer-Service.git)
cd Tanyain-Customer-Service

2. Install Dependencies
pip install flask flask_sqlalchemy flask_cors scikit-learn requests qrcode werkzeug

3. Environment Configuration
Create environment variables on your server or hosting provider (e.g., Replit Secrets, Vercel, or local .env):
SECRET_KEY=your_random_secure_secret_key
MAKE_WEBHOOK_URL=[https://hook.us1.make.com/your_webhook_id](https://hook.us1.make.com/your_webhook_id)

4. Run Application
python app.py
Access the application at http://127.0.0.1:5000/.

👤 Role Access Matrix
-Super Admin (/superadmin): Review, verify, and approve newly registered business merchant accounts.

-Client / Merchant (/dashboard): Manage FAQ knowledge base (CRUD/CSV Upload), view chat analytics, and download dynamic store QR codes.

-End User / Customer (/chat/<tenant_slug>): Public chat interface for instant AI support and automated order placement.

📜 License & Author
Developed with ❤️ by Rizky Juni Arigayo
