"""
ShopMind AI - Streamlit Frontend
Professional E-Commerce Intelligence Platform
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from pathlib import Path
import time

# ========== Config ==========
API_URL = "http://localhost:8000/api/v1"
st.set_page_config(
    page_title="ShopMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Neon AI SaaS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #0f172a 50%, #1a1035 100%);
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    
    .main-header {
        background: linear-gradient(90deg, #00d4ff, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #94a3b8;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        border-color: rgba(0, 212, 255, 0.5);
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.2);
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4ff, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .kpi-label {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }
    
    .section-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(168, 85, 247, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #a855f7) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4) !important;
    }
    
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1a1035 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.15);
    }
    
    .opportunity-high {
        border-left: 4px solid #ec4899;
        background: rgba(236, 72, 153, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .opportunity-medium {
        border-left: 4px solid #a855f7;
        background: rgba(168, 85, 247, 0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .metric-good { color: #22c55e; }
    .metric-warn { color: #f59e0b; }
    .metric-bad { color: #ef4444; }
</style>
""", unsafe_allow_html=True)

# ========== Session State ==========
if "workspace_id" not in st.session_state:
    st.session_state.workspace_id = None
if "dataset_id" not in st.session_state:
    st.session_state.dataset_id = None
if "dataset_info" not in st.session_state:
    st.session_state.dataset_info = None
if "page" not in st.session_state:
    st.session_state.page = "welcome"

def api_get(endpoint):
    try:
        r = requests.get(f"{API_URL}{endpoint}", timeout=30)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def api_post(endpoint, data=None, files=None):
    try:
        if files:
            r = requests.post(f"{API_URL}{endpoint}", files=files, timeout=120)
        else:
            r = requests.post(f"{API_URL}{endpoint}", json=data, timeout=30)
        if r.status_code in [200, 201]:
            return r.json()
        st.error(f"Error {r.status_code}: {r.text}")
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# ========== Pages ==========
def page_welcome():
    st.markdown('<div class="main-header">ShopMind AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">E-Commerce Sales, Customer Intelligence & Recommendation System<br>From Data → Story → Decision → Action</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="section-card" style="text-align:center;">
            <p style="color:#cbd5e1; font-size:1.05rem;">
            An adaptive AI-powered business intelligence platform that transforms your e-commerce data 
            into automated analytics, customer intelligence, predictions, product recommendations, 
            and actionable business insights.
            </p>
            <p style="color:#00d4ff; font-weight:600; margin-top:1rem;">
            "Your Data Knows Your Business. ShopMind Helps You Understand It."
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Quick Start")
    
    with st.form("business_form"):
        col1, col2 = st.columns(2)
        with col1:
            business_name = st.text_input("Business Name", value="My Online Store")
            industry = st.selectbox("Industry", ["E-commerce", "Fashion", "Electronics", "Marketplace", "Retail", "Other"])
        with col2:
            currency = st.selectbox("Currency", ["PKR", "USD", "EUR", "GBP", "INR"])
        
        submitted = st.form_submit_button("Start Your Business Analysis →", use_container_width=True)
        
        if submitted:
            with st.spinner("Creating workspace..."):
                result = api_post("/business", {
                    "business_name": business_name,
                    "industry": industry,
                    "currency": currency
                })
                if result:
                    st.session_state.workspace_id = result["workspace_id"]
                    st.session_state.page = "upload"
                    st.success(f"Workspace created: {result['workspace_id']}")
                    st.rerun()
    
    st.markdown("---")
    st.markdown("### ✨ Platform Capabilities")
    
    cols = st.columns(4)
    features = [
        ("📊", "Sales Intelligence", "Trends, categories, top products, geographic analysis"),
        ("👥", "Customer Universe", "RFM segmentation, CLV, churn prediction, Customer 360"),
        ("🎯", "Recommendations", "Hybrid engine, market basket, cross-sell opportunities"),
        ("🔮", "Future Lens", "Sales forecasting, opportunity radar, AI business copilot")
    ]
    for i, (icon, title, desc) in enumerate(features):
        with cols[i]:
            st.markdown(f"""
            <div class="section-card" style="text-align:center; min-height:140px;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="color:#00d4ff; font-weight:600; margin:0.5rem 0;">{title}</div>
                <div style="color:#94a3b8; font-size:0.85rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

def page_upload():
    st.markdown("## 📂 Dataset Upload")
    st.markdown(f"Workspace: `{st.session_state.workspace_id}`")
    
    st.info("Upload a CSV or Excel file with your e-commerce transaction data. The system will automatically detect schema and activate relevant intelligence modules.")
    
    # Sample data option
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded = st.file_uploader("Drag & drop your CSV/XLSX file", type=["csv", "xlsx", "xls"])
    with col2:
        st.markdown("#### Or use sample data")
        if st.button("Load Sample E-commerce Dataset", use_container_width=True):
            sample_path = Path("data/sample_ecommerce.csv")
            if sample_path.exists():
                with open(sample_path, "rb") as f:
                    files = {"file": ("sample_ecommerce.csv", f, "text/csv")}
                    with st.spinner("Processing sample dataset..."):
                        result = api_post(f"/upload/{st.session_state.workspace_id}", files=files)
                        if result:
                            st.session_state.dataset_id = result["dataset_id"]
                            st.session_state.dataset_info = result
                            st.session_state.page = "dashboard"
                            st.success("Sample data loaded successfully!")
                            st.rerun()
            else:
                st.error("Sample file not found")
    
    if uploaded:
        with st.spinner("Uploading and processing your data... This may take a moment."):
            files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
            result = api_post(f"/upload/{st.session_state.workspace_id}", files=files)
            if result:
                st.session_state.dataset_id = result["dataset_id"]
                st.session_state.dataset_info = result
                st.success(f"✅ Processed {result['summary']['rows']} rows successfully!")
                
                # Show mapping & modules
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Column Mapping")
                    st.json(result["summary"]["columns_mapped"])
                with col2:
                    st.markdown("#### Available Modules")
                    for m in result["summary"]["available_modules"]:
                        st.markdown(f"- `{m}`")
                
                if st.button("Go to Intelligence Dashboard →", use_container_width=True):
                    st.session_state.page = "dashboard"
                    st.rerun()

def render_kpi_row(kpis):
    cols = st.columns(6)
    items = [
        ("Total Revenue", f"{kpis.get('total_revenue', 0):,.0f}", "💰"),
        ("Orders", f"{kpis.get('total_orders', 0):,}", "🛒"),
        ("Customers", f"{kpis.get('unique_customers', 0):,}", "👥"),
        ("Products", f"{kpis.get('unique_products', 0):,}", "📦"),
        ("AOV", f"{kpis.get('average_order_value', 0):,.1f}", "📈"),
        ("Growth", f"{kpis.get('revenue_growth_pct', 'N/A')}%", "📉" if (kpis.get('revenue_growth_pct') or 0) < 0 else "📊"),
    ]
    for i, (label, value, icon) in enumerate(items):
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size:1.2rem;">{icon}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

def page_dashboard():
    ds = st.session_state.dataset_id
    if not ds:
        st.warning("No dataset loaded")
        return
    
    st.markdown("## 🏠 Executive Overview")
    
    data = api_get(f"/intelligence/{ds}/overview")
    if not data:
        return
    
    render_kpi_row(data["kpis"])
    
    st.markdown("---")
    
    # Business DNA
    dna = data.get("business_dna", {})
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Repeat Purchase Rate", f"{dna.get('repeat_purchase_rate_pct', 'N/A')}%")
    with col2:
        st.metric("Top 20% Customer Revenue", f"{dna.get('top20_customer_revenue_pct', 'N/A')}%")
    with col3:
        st.metric("Product Diversity", dna.get("product_diversity", "N/A"))
    with col4:
        st.metric("Data Coverage (days)", dna.get("data_coverage_days", "N/A"))
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Revenue Trend")
        trends = data.get("sales_trends", [])
        if trends:
            tdf = pd.DataFrame(trends)
            fig = px.area(tdf, x="period", y="revenue", 
                         color_discrete_sequence=["#00d4ff"])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                margin=dict(l=20, r=20, t=30, b=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏷️ Category Performance")
        cats = data.get("category_performance", [])
        if cats:
            cdf = pd.DataFrame(cats)
            fig = px.bar(cdf, x="category", y="revenue", color="revenue",
                        color_continuous_scale=["#1e3a5f", "#00d4ff", "#a855f7"])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                showlegend=False,
                margin=dict(l=20, r=20, t=30, b=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Top products & geo
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🏆 Top Products")
        tops = data.get("top_products", [])
        if tops:
            st.dataframe(pd.DataFrame(tops)[["product_id", "revenue", "quantity", "order_id"]].head(8), 
                        use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 📍 Geographic Analysis")
        geo = data.get("geographic", [])
        if geo:
            st.dataframe(pd.DataFrame(geo).head(8), use_container_width=True, hide_index=True)

def page_rfm():
    ds = st.session_state.dataset_id
    st.markdown("## 👥 Customer Universe — RFM Intelligence")
    
    data = api_get(f"/intelligence/{ds}/rfm")
    if not data:
        return
    
    st.markdown(f"**Total Customers Analyzed:** {data['total_customers']}")
    
    # Segment cards
    segments = data.get("segments", [])
    if segments:
        cols = st.columns(min(6, len(segments)))
        colors = ["#22c55e", "#00d4ff", "#a855f7", "#f59e0b", "#f97316", "#ef4444"]
        for i, seg in enumerate(segments):
            with cols[i % len(cols)]:
                st.markdown(f"""
                <div class="kpi-card">
                    <div style="color:{colors[i % len(colors)]}; font-weight:600; font-size:0.9rem;">{seg['Segment']}</div>
                    <div class="kpi-value" style="font-size:1.4rem;">{seg['customers']}</div>
                    <div class="kpi-label">{seg.get('revenue_pct', 0)}% revenue</div>
                    <div class="kpi-label">Avg spend: {seg.get('avg_spend', 0):,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Segment distribution chart
        sdf = pd.DataFrame(segments)
        fig = px.pie(sdf, values="customers", names="Segment", 
                    color_discrete_sequence=["#22c55e", "#00d4ff", "#a855f7", "#f59e0b", "#f97316", "#ef4444"])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Segment Details")
        st.dataframe(sdf, use_container_width=True, hide_index=True)

def page_churn():
    ds = st.session_state.dataset_id
    st.markdown("## ⚠️ Churn Prediction")
    
    with st.spinner("Training churn model..."):
        data = api_get(f"/intelligence/{ds}/churn")
    
    if not data:
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Method", data.get("method", "N/A"))
    with col2:
        st.metric("Churn Rate", f"{data.get('churn_rate', 0)*100:.1f}%")
    with col3:
        st.metric("Customers Analyzed", data.get("total_customers", 0))
    
    if data.get("metrics") and "roc_auc" in data["metrics"]:
        st.markdown("#### Model Performance")
        m = data["metrics"]
        cols = st.columns(4)
        cols[0].metric("ROC-AUC", m.get("roc_auc"))
        cols[1].metric("Precision", m.get("precision"))
        cols[2].metric("Recall", m.get("recall"))
        cols[3].metric("F1 Score", m.get("f1"))
    
    st.markdown("#### Risk Distribution")
    risk = data.get("risk_distribution", {})
    if risk:
        rdf = pd.DataFrame([{"Risk": k, "Count": v} for k, v in risk.items()])
        fig = px.bar(rdf, x="Risk", y="Count", color="Risk",
                    color_discrete_map={"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"})
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                         font_color="#e2e8f0", showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### High Risk Customers")
    high = data.get("high_risk_customers", [])
    if high:
        st.dataframe(pd.DataFrame(high), use_container_width=True, hide_index=True)
    
    if data.get("feature_importance"):
        st.markdown("#### Feature Importance")
        fi = data["feature_importance"]
        fidf = pd.DataFrame([{"Feature": k, "Importance": v} for k, v in fi.items()])
        fig = px.bar(fidf.sort_values("Importance"), x="Importance", y="Feature", orientation="h",
                    color_discrete_sequence=["#a855f7"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                         font_color="#e2e8f0", height=300)
        st.plotly_chart(fig, use_container_width=True)

def page_forecast():
    ds = st.session_state.dataset_id
    st.markdown("## 🔮 Future Lens — Sales Forecasting")
    
    horizon = st.slider("Forecast Horizon (days)", 15, 90, 30)
    
    data = api_get(f"/intelligence/{ds}/forecast?horizon={horizon}")
    if not data or "error" in data:
        st.warning(data.get("error", "Forecast unavailable") if data else "Failed")
        return
    
    summary = data.get("summary", {})
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Forecast Revenue", f"{summary.get('total_forecast_revenue', 0):,.0f}")
    col2.metric("Avg Daily Forecast", f"{summary.get('avg_daily_forecast', 0):,.1f}")
    col3.metric("Trend", summary.get("trend_direction", "N/A").title())
    
    # Combined chart
    hist = pd.DataFrame(data.get("historical", []))
    fut = pd.DataFrame(data.get("forecast", []))
    
    fig = go.Figure()
    if not hist.empty:
        fig.add_trace(go.Scatter(x=hist["date"], y=hist["revenue"], name="Actual",
                                line=dict(color="#00d4ff", width=2)))
    if not fut.empty:
        fig.add_trace(go.Scatter(x=fut["date"], y=fut["revenue"], name="Forecast",
                                line=dict(color="#a855f7", width=2, dash="dash")))
        if "lower" in fut.columns:
            fig.add_trace(go.Scatter(x=fut["date"], y=fut["upper"], fill=None, mode="lines",
                                    line=dict(width=0), showlegend=False))
            fig.add_trace(go.Scatter(x=fut["date"], y=fut["lower"], fill="tonexty", mode="lines",
                                    line=dict(width=0), fillcolor="rgba(168,85,247,0.2)",
                                    name="Confidence Band"))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0", height=400,
        title="Historical Sales + Forecast",
        xaxis_title="Date", yaxis_title="Revenue"
    )
    st.plotly_chart(fig, use_container_width=True)

def page_recommendations():
    ds = st.session_state.dataset_id
    st.markdown("## 🎯 Product Recommendations & Market Basket")
    
    data = api_get(f"/intelligence/{ds}/recommendations")
    if not data:
        return
    
    tab1, tab2 = st.tabs(["Business Opportunities", "Association Rules"])
    
    with tab1:
        opps = data.get("business_opportunities", [])
        if opps:
            st.dataframe(pd.DataFrame(opps), use_container_width=True, hide_index=True)
        else:
            st.info("No business recommendations available")
    
    with tab2:
        assoc = data.get("associations", {})
        rules = assoc.get("rules", [])
        st.markdown(f"Method: `{assoc.get('method', 'N/A')}`")
        if rules:
            st.dataframe(pd.DataFrame(rules), use_container_width=True, hide_index=True)
        else:
            st.info("No strong associations found")

def page_opportunities():
    ds = st.session_state.dataset_id
    st.markdown("## 📡 Opportunity Radar")
    
    data = api_get(f"/intelligence/{ds}/opportunity-radar")
    if not data:
        return
    
    st.markdown(f"**{data.get('count', 0)} opportunities detected**")
    
    for opp in data.get("opportunities", []):
        impact_class = "opportunity-high" if opp.get("impact") == "high" else "opportunity-medium"
        st.markdown(f"""
        <div class="{impact_class}">
            <div style="font-weight:600; color:#e2e8f0;">{opp.get('title')}</div>
            <div style="color:#94a3b8; margin:0.3rem 0;">{opp.get('description')}</div>
            <div style="color:#64748b; font-size:0.8rem;">Type: {opp.get('type')} · Impact: {opp.get('impact')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if opp.get("evidence"):
            with st.expander("View Evidence"):
                st.json(opp["evidence"][:5] if isinstance(opp["evidence"], list) else opp["evidence"])

def page_copilot():
    ds = st.session_state.dataset_id
    st.markdown("## 🤖 AI Business Copilot")
    st.markdown("Ask questions about your business data. The copilot answers using verified metrics.")
    
    examples = [
        "What is my total revenue?",
        "How are my customers segmented?",
        "What are my top products?",
        "What is the sales forecast?",
        "What is my churn risk?"
    ]
    
    st.markdown("**Try asking:**")
    cols = st.columns(len(examples))
    for i, ex in enumerate(examples):
        if cols[i].button(ex, key=f"ex_{i}"):
            st.session_state.copilot_q = ex
    
    question = st.text_input("Your question", value=st.session_state.get("copilot_q", ""))
    
    if st.button("Ask ShopMind", use_container_width=True) and question:
        with st.spinner("Analyzing..."):
            result = api_post(f"/intelligence/{ds}/ask", {
                "question": question,
                "workspace_id": st.session_state.workspace_id or "demo"
            })
            if result:
                st.markdown(f"""
                <div class="section-card">
                    <div style="color:#94a3b8; font-size:0.85rem;">Question</div>
                    <div style="color:#e2e8f0; margin-bottom:1rem;">{result.get('question')}</div>
                    <div style="color:#94a3b8; font-size:0.85rem;">Answer</div>
                    <div style="color:#00d4ff; font-size:1.1rem;">{result.get('answer')}</div>
                    <div style="color:#64748b; font-size:0.75rem; margin-top:0.8rem;">
                        Metrics used: {', '.join(result.get('metrics_used', []))}
                    </div>
                </div>
                """, unsafe_allow_html=True)

def page_clv():
    ds = st.session_state.dataset_id
    st.markdown("## 💎 Customer Lifetime Value (CLV)")
    
    data = api_get(f"/intelligence/{ds}/clv")
    if not data:
        return
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Historical Value", f"{data.get('avg_historical_value', 0):,.0f}")
    col2.metric("Avg Predicted CLV (12m)", f"{data.get('avg_predicted_clv', 0):,.0f}")
    col3.metric("Customers", data.get("total_customers", 0))
    
    st.markdown("#### CLV Distribution")
    dist = data.get("clv_distribution", {})
    if dist:
        cols = st.columns(5)
        cols[0].metric("Min", f"{dist.get('min', 0):,.0f}")
        cols[1].metric("P25", f"{dist.get('p25', 0):,.0f}")
        cols[2].metric("Median", f"{dist.get('median', 0):,.0f}")
        cols[3].metric("P75", f"{dist.get('p75', 0):,.0f}")
        cols[4].metric("Max", f"{dist.get('max', 0):,.0f}")
    
    st.markdown("#### Top Customers by Predicted CLV")
    tops = data.get("top_customers", [])
    if tops:
        st.dataframe(pd.DataFrame(tops), use_container_width=True, hide_index=True)
    
    seg = data.get("segment_distribution", {})
    if seg:
        st.markdown("#### CLV Segments")
        sdf = pd.DataFrame([{"Segment": k, "Count": v} for k, v in seg.items()])
        fig = px.pie(sdf, values="Count", names="Segment",
                    color_discrete_sequence=["#64748b", "#00d4ff", "#a855f7", "#ec4899"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", height=300)
        st.plotly_chart(fig, use_container_width=True)

# ========== Navigation ==========
def main():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:1rem 0;">
            <div style="font-size:1.8rem; font-weight:700; 
                background: linear-gradient(90deg, #00d4ff, #a855f7, #ec4899);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ShopMind AI
            </div>
            <div style="color:#64748b; font-size:0.75rem;">Intelligence Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.session_state.workspace_id:
            st.markdown(f"**Workspace:** `{st.session_state.workspace_id}`")
        if st.session_state.dataset_id:
            st.markdown(f"**Dataset:** `{st.session_state.dataset_id}`")
            st.markdown("---")
            
            pages = {
                "🏠 Overview": "dashboard",
                "👥 RFM Segments": "rfm",
                "💎 Customer CLV": "clv",
                "⚠️ Churn Risk": "churn",
                "🔮 Sales Forecast": "forecast",
                "🎯 Recommendations": "recommendations",
                "📡 Opportunity Radar": "opportunities",
                "🤖 AI Copilot": "copilot",
            }
            
            for label, page_id in pages.items():
                if st.button(label, use_container_width=True, key=f"nav_{page_id}"):
                    st.session_state.page = page_id
                    st.rerun()
        
        st.markdown("---")
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.workspace_id = None
            st.session_state.dataset_id = None
            st.session_state.dataset_info = None
            st.session_state.page = "welcome"
            st.rerun()
    
    # Route
    page = st.session_state.page
    if page == "welcome" or not st.session_state.workspace_id:
        page_welcome()
    elif page == "upload" or not st.session_state.dataset_id:
        page_upload()
    elif page == "dashboard":
        page_dashboard()
    elif page == "rfm":
        page_rfm()
    elif page == "clv":
        page_clv()
    elif page == "churn":
        page_churn()
    elif page == "forecast":
        page_forecast()
    elif page == "recommendations":
        page_recommendations()
    elif page == "opportunities":
        page_opportunities()
    elif page == "copilot":
        page_copilot()
    else:
        page_dashboard()

if __name__ == "__main__":
    main()
