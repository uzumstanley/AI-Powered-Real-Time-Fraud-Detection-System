🚀 Just Launched: End-to-End Real-Time Fraud Detection System! 🚀

I'm excited to share my latest project—a full-stack, real-time fraud detection platform built from scratch! This project demonstrates my expertise in data engineering, machine learning, backend API development, and modern frontend engineering.

What I built:

🔹 Data Engineering & Feature Engineering:
* Designed a robust PostgreSQL schema to store and manage transaction data.
* Engineered features such as transaction statistics, user behavior metrics, and categorical encodings to maximize fraud detection accuracy.

🔹 Machine Learning:
* Developed and trained an unsupervised Isolation Forest model for anomaly detection using scikit-learn.
* Built a preprocessing pipeline with scaling and one-hot encoding to ensure consistent, production-ready inference.
* Automated model serialization and deployment using joblib.

🔹 Backend API (FastAPI):
* Built RESTful endpoints for transaction ingestion and real-time fraud scoring.
* Integrated the ML model and preprocessing pipeline for seamless, low-latency predictions.
* Implemented robust error handling, CORS support, and database integration.

🔹 Frontend (React):
* Developed an intuitive dashboard to visualize transactions, fraud alerts, and scoring results in real time.
* Built a transaction scoring form for instant feedback and model transparency.
* Leveraged Axios for smooth API communication and React hooks for state management.

🔹 Testing & DevOps:
* Wrote comprehensive unit tests for both backend and frontend.
* Used environment variables and .env files for secure, configurable deployments.
* Ensured full system alignment with automated integration tests.

Tech Stack: Python, FastAPI, scikit-learn, PostgreSQL, React, Axios, Docker, pgAdmin

Key Skills Demonstrated:
* End-to-end ML system design
* API development & integration
* Database modeling
* Frontend engineering
* Automated testing & CI/CD best practices

This project is an end-to-end real-time fraud detection platform featuring a machine learning backend (Python/FastAPI), a PostgreSQL database, and a modern React frontend dashboard.

---

## 🚀 Features

- **Real-time transaction ingestion and scoring**
- **Isolation Forest anomaly detection model**
- **Feature engineering and preprocessing pipeline**
- **RESTful API with FastAPI**
- **PostgreSQL for persistent storage**
- **Interactive React dashboard for monitoring and scoring**
- **Unit and integration tests**

---

## 🛠️ Prerequisites

- Python 3.8+
- Node.js & npm
- PostgreSQL
- (Optional) Redis (if using caching)
- [pgAdmin](https://www.pgadmin.org/) or psql for database management

---

## ⚡ Quick Start

### 1. **Clone the Repository**

```bash
git clone https://github.com/uzumstanley/AI-Powered-Real-Time-Fraud-Detection-System.git
cd AI-Powered-Real-Time-Fraud-Detection-System
```

### 2. **Set Up the Database**

- Create a PostgreSQL database (e.g., `frauddb`).
- Create a user (e.g., `mac`) with access.
- Run the schema:

```bash
psql -U mac -d frauddb -f app/Database/schema.sql
```

### 3. **Configure Environment Variables**

Edit `app/.env`:

```
DATABASE_URL=postgresql://mac@localhost:5432/frauddb
JWT_SECRET=your_jwt_secret_here
```

### 4. **Install Python Dependencies**

```bash
cd app
pip install -r ../requirements.txt
```

### 5. **Start the Backend**

```bash
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 6. **Run Tests (Optional)**

```bash
pytest ../tests/test_main.py
```

### 7. **Start the Frontend**

```bash
cd ../frontend
npm install
npm start
```

The dashboard will be available at [http://localhost:3000](http://localhost:3000).

---

## 🖥️ Usage

- **Score a transaction:** Use the form on the dashboard or send a POST request to `/transactions/score` with JSON data.
- **View transactions:** The dashboard lists recent transactions and fraud alerts.
- **API docs:** Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

---

## 📄 Sample Transaction JSON

```json
{
  "account_id": "test_account_123",
  "TransactionAmount": 420.50,
  "CustomerAge": 35,
  "TransactionDuration": 6.2,
  "LoginAttempts": 1,
  "AccountBalance": 15000.0,
  "user_transaction_count": 8,
  "user_avg_transaction_amount": 400.0,
  "deviation_from_user_avg": 20.5,
  "transaction_hour": 10,
  "transaction_day_of_week": 1,
  "TransactionType": "Debit",
  "Location": "Chicago",
  "Channel": "Online",
  "CustomerOccupation": "Analyst",
  "user_primary_location": "Chicago",
  "is_unusual_location": "False"
}

you can score the transactions with task specific data
```

---

## 🧑‍💻 Project Structure

```
app/                # FastAPI backend and ML model
frontend/           # React frontend
tests/              # Unit and integration tests
app/Database/       # Database schema
app/model/          # Model training and conversion scripts
```

---
Feel free to DM me for a walkthrough or collaboration opportunities!

Project Roadmap: https://github.com/users/uzumstanley/projects/2/views/1


## 🙋‍♂️ Contact

For questions or collaboration, open an issue or contact [uzumstanley](https://github.com/uzumstanley).

