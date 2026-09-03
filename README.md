# ShopMind AI

**E-Commerce Sales & Customer Intelligence Recommendation System**
*Understand customers. Predict demand. Recommend smarter.*

This repository contains the front-end product experience for ShopMind AI — a SaaS-style e-commerce analytics platform. It includes the landing page, authentication screen, and a 13-module intelligence dashboard, built as a single interactive web app (no build step required).

---

## 1. What's Included

| File | Purpose |
|---|---|
| `index.html` | Landing page, sign-in page, and app shell (sidebar + layout) |
| `app.js` | All app logic: navigation, demo data, chart rendering, and the 13 dashboard modules |
| `README.md` | This file |

**No installation, framework, or build tools are required.** It's plain HTML, CSS, and JavaScript, using CDN-hosted libraries:
- [Chart.js](https://www.chartjs.org/) — charts (line, bar, doughnut, bubble)
- [PapaParse](https://www.papaparse.com/) — CSV parsing for the Data Center upload
- [Font Awesome](https://fontawesome.com/) — icons
- Google Fonts (Manrope + Inter)

## 2. Modules Included

1. **Overview** — revenue, orders, active customers, AOV, repeat rate, growth, top products, AI insights
2. **Sales Intelligence** — revenue trend, category performance, regional revenue, hourly heatmap
3. **Customer 360°** — customer profile, purchase history, spend trend, preferences
4. **Segmentation (RFM)** — recency/frequency/monetary scoring, segment distribution
5. **Churn Intelligence** — churn risk distribution, at-risk customer list, retention actions
6. **Product Intelligence** — performance matrix, top sellers, low performers
7. **Recommendations** — personalized product suggestions with match score and reasoning
8. **Sales Forecasting** — 30-day forecast with confidence interval (upper/lower bound)
9. **Customer Value (CLV)** — average/total CLV, value tiers, top high-value customers
10. **AI Business Assistant** — chat-style Q&A interface over business data
11. **Data Center** — drag-and-drop CSV upload with live parsing preview and data-quality score
12. **Model Performance** — churn/forecast model comparison, confusion matrix, precision/recall/F1
13. **Settings** — profile, preferences, data controls

## 3. Running Locally

No server is strictly required — you can open `index.html` directly in a browser. For full compatibility (some browsers restrict local file access for scripts), run a simple local server:

```bash
# Python (already installed on most systems)
cd shopmind-ai
python3 -m http.server 8000
# then open http://localhost:8000
```

or, with Node.js:

```bash
npx serve .
```

## 4. Deployment Guide

Because this is a fully static app, it can be deployed for free on any static host in under 5 minutes.

### Option A — Vercel (recommended)
1. Create a free account at [vercel.com](https://vercel.com).
2. Click **Add New → Project → Upload** (or connect a GitHub repo containing these files).
3. Leave the framework preset as **Other** — no build command is needed.
4. Click **Deploy**. Vercel will give you a live URL (e.g. `shopmind-ai.vercel.app`).

### Option B — Netlify
1. Create a free account at [netlify.com](https://netlify.com).
2. Go to **Sites → Add new site → Deploy manually**.
3. Drag and drop the folder containing `index.html` and `app.js`.
4. Netlify deploys instantly and gives you a live URL.

### Option C — GitHub Pages
1. Push `index.html` and `app.js` to a GitHub repository.
2. Go to **Settings → Pages**.
3. Under **Source**, select the `main` branch and `/ (root)` folder.
4. Save — your site will be live at `https://<username>.github.io/<repo-name>/`.

> No environment variables, API keys, or backend are required for this front-end version — everything runs client-side with demo/generated data, matching the current phase of the project.

## 5. Roadmap (Full Proposal Scope)

This front-end build corresponds to the **UI/UX and application-shell phase** of the full ShopMind AI proposal. The complete system (per the project proposal) additionally includes:

- CSV/Excel upload → automated validation, cleaning, transformation, feature engineering
- RFM + K-Means customer segmentation (real clustering, not demo data)
- Churn prediction (Logistic Regression, Random Forest, XGBoost/LightGBM)
- CLV estimation (baseline + optional BG/NBD & Gamma-Gamma)
- Hybrid recommendation engine (popularity, content-based, collaborative filtering)
- Sales forecasting (Prophet / gradient boosting) with chronological validation
- AI Business Assistant grounded in real computed analytics
- Backend: Python, Pandas/NumPy, Scikit-learn, FastAPI (optional), PostgreSQL

These are planned for the next development phase, where the current front-end will be connected to a real data pipeline and trained models instead of demo data.

## 6. Important Note on Data

All charts and figures currently shown (revenue, customers, churn %, etc.) are **illustrative demo data** generated in the browser to visualize the product experience — consistent with the proposal's scope rule that the app should never fabricate or claim real business results before a dataset is connected.

---
Built for **Kinza Arshad** — Data Science Portfolio Project.
