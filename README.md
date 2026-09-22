# 🧠 ShopMind AI

**E-Commerce Sales, Customer Intelligence & Recommendation System**

> *Your Data Knows Your Business. ShopMind Helps You Understand It.*

An adaptive AI-powered business intelligence platform that transforms uploaded e-commerce data into automated analytics, customer intelligence, predictions, product recommendations, and actionable business insights.

**From Data → Story → Decision → Action**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?logo=scikitlearn)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### Core Intelligence Modules

| Module | Description |
|--------|-------------|
| **Adaptive Data Engine** | Automatic schema detection, validation, cleaning & profiling for CSV/XLSX |
| **Executive Overview** | KPIs, Business DNA, revenue trends, category & geographic analysis |
| **Sales Intelligence** | Daily/weekly/monthly trends, period comparisons, product performance |
| **RFM Customer Universe** | Champions, Loyal Core, Rising Stars, New Arrivals, Slipping Away, Dormant |
| **Customer Lifetime Value** | Historical + predictive 12-month CLV with segmentation |
| **Churn Prediction** | Random Forest / rule-based risk scoring with feature importance |
| **Future Lens** | Sales forecasting with confidence bands (15–90 day horizons) |
| **Product Recommendations** | Collaborative + association-based hybrid engine |
| **Market Basket Analysis** | Apriori / co-occurrence rules with support, confidence, lift |
| **Opportunity Radar** | Actionable signals for retention, cross-sell, growth & product opportunities |
| **AI Business Copilot** | Natural language Q&A over verified platform metrics |

### Design System

- **Theme**: Deep Navy + Neon Blue + Electric Purple + Neon Pink
- **Style**: Modern AI-SaaS with glassmorphism-inspired cards
- **Charts**: Interactive Plotly visualizations
- **UX**: Guided journey — Upload → Analyze → Discover → Predict → Act

---

## 🏗️ Architecture

```
shopmind-ai/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py           # API routes & application entry
│   │   ├── core/             # Config, security
│   │   └── services/         # Business logic & ML
│   │       ├── data_engine.py
│   │       ├── analytics.py
│   │       ├── rfm.py
│   │       └── ml_models.py  # CLV, Churn, Forecast, Recs
│   ├── requirements.txt
│   └── Dockerfile
├── data/
│   └── sample_ecommerce.csv  # Ready-to-use demo dataset
├── streamlit_app.py          # Professional frontend
├── docker-compose.yml
└── README.md
```

**Tech Stack**

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11 + FastAPI |
| Frontend | Streamlit (neon AI theme) |
| Data Processing | Pandas + NumPy |
| Machine Learning | scikit-learn, XGBoost, LightGBM |
| Association Rules | mlxtend (Apriori) |
| Visualization | Plotly |
| Containerization | Docker + Docker Compose |

---

## 🚀 Quick Start

### Option 1: Local (Recommended for development)

**Prerequisites:** Python 3.11+, pip

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/shopmind-ai.git
cd shopmind-ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# 4. Install frontend dependencies
pip install streamlit plotly requests

# 5. Start the API server (Terminal 1)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 6. Start the frontend (Terminal 2)
streamlit run streamlit_app.py
```

Open **http://localhost:8501** in your browser.

### Option 2: Docker

```bash
docker-compose up --build
```

API will be available at `http://localhost:8000`  
(You can still run Streamlit locally against the containerized API)

---

## 📊 Demo Walkthrough

1. **Welcome Screen** → Enter business name and click **Start Your Business Analysis**
2. **Upload** → Click **Load Sample E-commerce Dataset** (or upload your own CSV/XLSX)
3. **Dashboard** → Explore KPIs, trends, categories, and top products
4. **RFM Segments** → View customer segments and revenue contribution
5. **CLV** → See predicted customer lifetime value distribution
6. **Churn Risk** → Identify high-risk customers with model metrics
7. **Sales Forecast** → 30/60/90-day revenue projections
8. **Recommendations** → Association rules and product opportunities
9. **Opportunity Radar** → Prioritized business signals
10. **AI Copilot** → Ask natural language questions about your data

---

## 📁 Preferred Dataset Schema

| Field | Purpose | Status |
|-------|---------|--------|
| `order_id` | Transaction identifier | **Core** |
| `customer_id` | Customer identifier | **Core** |
| `product_id` | Product/SKU identifier | **Core** |
| `product_name` | Product name | Useful |
| `category` | Product category | Useful |
| `quantity` | Units purchased | **Core** |
| `unit_price` / `revenue` | Transaction value | **Core** |
| `order_date` | Transaction date | **Core** |
| `location` | Geography | Optional |
| `discount` | Discount amount | Optional |
| `marketing_channel` | Acquisition source | Optional |
| `stock` | Inventory level | Optional |

The adaptive engine automatically maps common column name variations.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health & info |
| `POST` | `/api/v1/business` | Create workspace |
| `POST` | `/api/v1/upload/{workspace_id}` | Upload & process dataset |
| `GET` | `/api/v1/intelligence/{id}/overview` | Executive KPIs + DNA |
| `GET` | `/api/v1/intelligence/{id}/sales` | Full sales intelligence |
| `GET` | `/api/v1/intelligence/{id}/rfm` | RFM segmentation |
| `GET` | `/api/v1/intelligence/{id}/clv` | Customer lifetime value |
| `GET` | `/api/v1/intelligence/{id}/churn` | Churn prediction |
| `GET` | `/api/v1/intelligence/{id}/forecast` | Sales forecast |
| `GET` | `/api/v1/intelligence/{id}/recommendations` | Product recommendations |
| `GET` | `/api/v1/intelligence/{id}/market-basket` | Association rules |
| `GET` | `/api/v1/intelligence/{id}/opportunity-radar` | Opportunity signals |
| `POST` | `/api/v1/intelligence/{id}/ask` | AI Copilot Q&A |

Interactive docs available at **http://localhost:8000/docs**

---

## 🧪 Sample Dataset

A realistic sample dataset is included:

- **~9,150** transaction rows
- **500** customers
- **80** products across 7 categories
- Date range: Jan 2023 – Jun 2025
- Fields: order, customer, product, category, quantity, price, revenue, date, location, discount, marketing channel

---

## 🛠️ Development Roadmap (Aligned with Proposal)

- [x] Adaptive data engine (schema detection, validation, cleaning)
- [x] Executive Overview + Sales Intelligence
- [x] RFM Customer Segmentation
- [x] Customer Lifetime Value
- [x] Churn Prediction (RF + rule-based fallback)
- [x] Sales Forecasting
- [x] Hybrid Recommendations + Market Basket
- [x] Opportunity Radar
- [x] AI Business Copilot
- [x] Professional neon AI-SaaS UI
- [x] Docker support
- [ ] PostgreSQL + Redis production mode
- [ ] Full React + Tailwind frontend (current Streamlit is production-ready alternative)
- [ ] JWT authentication & multi-user workspaces
- [ ] PDF report generation
- [ ] What-If Simulator
- [ ] Model Center with versioning

---

## 🔒 Data Privacy & Reliability

- Never hard-codes metrics — everything is computed from uploaded data
- Clearly indicates when a module cannot run due to missing fields
- Separates raw and processed data
- Displays uncertainty for forecasts and CLV estimates
- No external AI services receive your raw customer data

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

Built as a complete portfolio-grade Data Science / Full-Stack AI project demonstrating:

- Data Engineering & Adaptive Pipelines
- Classical ML + Forecasting
- Recommendation Systems
- API Design with FastAPI
- Interactive Analytics UI
- Docker-based deployment

**ShopMind AI** — *From raw transactions to understandable insights, predictions, recommendations and practical next actions.*
