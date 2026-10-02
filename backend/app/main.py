"""
ShopMind AI - FastAPI Backend
E-Commerce Sales, Customer Intelligence & Recommendation System
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
import os
import uuid
import json
from datetime import datetime
from pathlib import Path
import shutil

from app.core.config import settings
from app.services.data_engine import DataEngine
from app.services.analytics import SalesAnalytics
from app.services.rfm import RFMEngine
from app.services.ml_models import CLVEngine, ChurnPredictor, SalesForecaster, RecommendationEngine

# Create directories
Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
Path(settings.PROCESSED_DIR).mkdir(exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Adaptive AI-powered e-commerce intelligence platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for demo (replace with PostgreSQL in production)
WORKSPACES: Dict[str, Dict] = {}
DATASETS: Dict[str, Dict] = {}

class BusinessCreate(BaseModel):
    business_name: str
    industry: Optional[str] = "E-commerce"
    currency: Optional[str] = "PKR"

class QueryRequest(BaseModel):
    question: str
    workspace_id: str

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "message": "Your Data Knows Your Business. ShopMind Helps You Understand It.",
        "docs": "/docs"
    }

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# ========== Business Workspace ==========
@app.post("/api/v1/business")
async def create_business(data: BusinessCreate):
    workspace_id = str(uuid.uuid4())[:8]
    WORKSPACES[workspace_id] = {
        "id": workspace_id,
        "business_name": data.business_name,
        "industry": data.industry,
        "currency": data.currency,
        "created_at": datetime.utcnow().isoformat(),
        "datasets": []
    }
    return {"workspace_id": workspace_id, "business": WORKSPACES[workspace_id]}

@app.get("/api/v1/business/{workspace_id}")
async def get_business(workspace_id: str):
    if workspace_id not in WORKSPACES:
        raise HTTPException(404, "Workspace not found")
    return WORKSPACES[workspace_id]

# ========== Dataset Upload & Processing ==========
@app.post("/api/v1/upload/{workspace_id}")
async def upload_dataset(workspace_id: str, file: UploadFile = File(...)):
    if workspace_id not in WORKSPACES:
        raise HTTPException(404, "Workspace not found")
    
    ext = Path(file.filename).suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Invalid file type. Allowed: {settings.ALLOWED_EXTENSIONS}")
    
    dataset_id = str(uuid.uuid4())[:8]
    file_path = Path(settings.UPLOAD_DIR) / f"{dataset_id}{ext}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise HTTPException(400, f"File too large. Max {settings.MAX_UPLOAD_SIZE_MB}MB")
        f.write(content)
    
    # Process
    engine = DataEngine()
    try:
        result = engine.process(str(file_path))
    except Exception as e:
        raise HTTPException(400, f"Processing failed: {str(e)}")
    
    # Save processed
    processed_path = Path(settings.PROCESSED_DIR) / f"{dataset_id}.parquet"
    engine.processed_df.to_parquet(processed_path)
    
    DATASETS[dataset_id] = {
        "id": dataset_id,
        "workspace_id": workspace_id,
        "filename": file.filename,
        "uploaded_at": datetime.utcnow().isoformat(),
        "file_path": str(file_path),
        "processed_path": str(processed_path),
        "column_mapping": result["column_mapping"],
        "data_health": result["data_health"],
        "profile": result["profile"],
        "available_modules": result["available_modules"],
        "processed_rows": result["processed_rows"]
    }
    
    WORKSPACES[workspace_id]["datasets"].append(dataset_id)
    
    return {
        "dataset_id": dataset_id,
        "status": "processed",
        "summary": {
            "rows": result["processed_rows"],
            "columns_mapped": result["column_mapping"],
            "available_modules": result["available_modules"],
            "data_health": result["data_health"],
            "profile": result["profile"]
        },
        "preview": result["preview"]
    }

@app.get("/api/v1/dataset/{dataset_id}")
async def get_dataset_info(dataset_id: str):
    if dataset_id not in DATASETS:
        raise HTTPException(404, "Dataset not found")
    return DATASETS[dataset_id]

def load_df(dataset_id: str) -> pd.DataFrame:
    if dataset_id not in DATASETS:
        raise HTTPException(404, "Dataset not found")
    path = DATASETS[dataset_id]["processed_path"]
    return pd.read_parquet(path)

# ========== Intelligence Endpoints ==========
@app.get("/api/v1/intelligence/{dataset_id}/overview")
async def executive_overview(dataset_id: str):
    df = load_df(dataset_id)
    analytics = SalesAnalytics(df)
    return {
        "kpis": analytics.executive_kpis(),
        "business_dna": analytics.business_dna(),
        "category_performance": analytics.category_performance()[:8],
        "top_products": analytics.top_products(8),
        "geographic": analytics.geographic_analysis()[:8],
        "sales_trends": analytics.sales_trends("M")
    }

@app.get("/api/v1/intelligence/{dataset_id}/sales")
async def sales_intelligence(dataset_id: str):
    df = load_df(dataset_id)
    analytics = SalesAnalytics(df)
    return {
        "kpis": analytics.executive_kpis(),
        "trends_monthly": analytics.sales_trends("M"),
        "trends_weekly": analytics.sales_trends("W"),
        "category_performance": analytics.category_performance(),
        "top_products": analytics.top_products(15),
        "geographic": analytics.geographic_analysis()
    }

@app.get("/api/v1/intelligence/{dataset_id}/rfm")
async def rfm_intelligence(dataset_id: str):
    df = load_df(dataset_id)
    if "customer_id" not in df.columns:
        raise HTTPException(400, "Customer ID required for RFM analysis")
    
    engine = RFMEngine(df)
    return engine.get_full_results()

@app.get("/api/v1/intelligence/{dataset_id}/clv")
async def clv_intelligence(dataset_id: str):
    df = load_df(dataset_id)
    if "customer_id" not in df.columns:
        raise HTTPException(400, "Customer ID required for CLV")
    
    engine = CLVEngine(df)
    return engine.calculate()

@app.get("/api/v1/intelligence/{dataset_id}/churn")
async def churn_prediction(dataset_id: str):
    df = load_df(dataset_id)
    if "customer_id" not in df.columns:
        raise HTTPException(400, "Customer ID required for churn prediction")
    
    predictor = ChurnPredictor(df)
    return predictor.train_and_predict()

@app.get("/api/v1/intelligence/{dataset_id}/forecast")
async def sales_forecast(dataset_id: str, horizon: int = 30):
    df = load_df(dataset_id)
    if "order_date" not in df.columns or "revenue" not in df.columns:
        raise HTTPException(400, "Order date and revenue required for forecasting")
    
    forecaster = SalesForecaster(df)
    return forecaster.forecast(horizon_days=horizon)

@app.get("/api/v1/intelligence/{dataset_id}/recommendations")
async def recommendations(dataset_id: str, customer_id: Optional[str] = None):
    df = load_df(dataset_id)
    engine = RecommendationEngine(df)
    
    result = {
        "associations": engine.product_associations(),
        "business_opportunities": engine.business_recommendations(10)
    }
    
    if customer_id:
        result["for_customer"] = engine.customer_recommendations(customer_id)
    
    return result

@app.get("/api/v1/intelligence/{dataset_id}/market-basket")
async def market_basket(dataset_id: str):
    df = load_df(dataset_id)
    engine = RecommendationEngine(df)
    return engine.product_associations(min_support=0.005)

@app.get("/api/v1/intelligence/{dataset_id}/opportunity-radar")
async def opportunity_radar(dataset_id: str):
    df = load_df(dataset_id)
    analytics = SalesAnalytics(df)
    rfm = RFMEngine(df) if "customer_id" in df.columns else None
    recs = RecommendationEngine(df)
    
    opportunities = []
    
    # High-value slipping customers
    if rfm:
        rfm_data = rfm.calculate()
        slipping = rfm_data[rfm_data["Segment"].isin(["Slipping Away", "Dormant"])]
        if len(slipping) > 0:
            high_value_slipping = slipping.nlargest(5, "monetary")
            opportunities.append({
                "type": "retention",
                "title": "High-value customers at risk",
                "description": f"{len(slipping)} customers in Slipping Away / Dormant segments. Top 5 represent significant revenue.",
                "impact": "high",
                "evidence": high_value_slipping[["customer_id", "monetary", "recency", "Segment"]].to_dict(orient="records")
            })
    
    # Association opportunities
    assoc = recs.product_associations()
    if assoc.get("rules"):
        opportunities.append({
            "type": "cross_sell",
            "title": "Strong product association opportunities",
            "description": f"Found {len(assoc['rules'])} product relationships for bundling and cross-sell.",
            "impact": "medium",
            "evidence": assoc["rules"][:5]
        })
    
    # Category growth
    cats = analytics.category_performance()
    if cats:
        opportunities.append({
            "type": "growth",
            "title": "Category performance insights",
            "description": f"Top category '{cats[0]['category']}' contributes {cats[0].get('revenue_pct', 0)}% of revenue.",
            "impact": "medium",
            "evidence": cats[:3]
        })
    
    # Hidden gems
    business_recs = recs.business_recommendations(5)
    if business_recs:
        opportunities.append({
            "type": "product",
            "title": "Hidden product opportunities",
            "description": "Products with strong repeat signals but room for growth.",
            "impact": "medium",
            "evidence": business_recs
        })
    
    return {"opportunities": opportunities, "count": len(opportunities)}

@app.post("/api/v1/intelligence/{dataset_id}/ask")
async def ai_copilot(dataset_id: str, query: QueryRequest):
    """Simple rule-based AI Copilot over metrics"""
    df = load_df(dataset_id)
    analytics = SalesAnalytics(df)
    kpis = analytics.executive_kpis()
    question = query.question.lower()
    
    response = {"question": query.question, "answer": "", "metrics_used": [], "type": "insight"}
    
    if "revenue" in question or "sales" in question:
        response["answer"] = (
            f"Total revenue is **{kpis['total_revenue']:,.2f}** across "
            f"**{kpis['total_orders']}** orders from **{kpis['unique_customers']}** customers. "
            f"Average order value is **{kpis['average_order_value']:,.2f}**."
        )
        if kpis.get("revenue_growth_pct") is not None:
            response["answer"] += f" Recent 30-day growth vs previous period: **{kpis['revenue_growth_pct']}%**."
        response["metrics_used"] = ["total_revenue", "total_orders", "unique_customers", "aov"]
    
    elif "customer" in question or "segment" in question or "rfm" in question:
        if "customer_id" in df.columns:
            rfm = RFMEngine(df)
            summary = rfm.get_segment_summary()
            top_seg = summary[0] if summary else {}
            response["answer"] = (
                f"You have **{kpis['unique_customers']}** unique customers. "
                f"Largest segment by value: **{top_seg.get('Segment', 'N/A')}** "
                f"({top_seg.get('customers', 0)} customers, {top_seg.get('revenue_pct', 0)}% of revenue)."
            )
            response["metrics_used"] = ["unique_customers", "rfm_segments"]
        else:
            response["answer"] = "Customer analysis requires a customer_id field in your data."
    
    elif "product" in question or "top" in question:
        tops = analytics.top_products(5)
        if tops:
            names = [f"{p.get('product_name', p['product_id'])} ({p['revenue']:,.0f})" for p in tops[:3]]
            response["answer"] = f"Top products by revenue: {', '.join(names)}."
            response["metrics_used"] = ["top_products"]
        else:
            response["answer"] = "Product data not available."
    
    elif "forecast" in question or "future" in question or "predict" in question:
        if "order_date" in df.columns:
            fc = SalesForecaster(df).forecast(30)
            if "summary" in fc:
                response["answer"] = (
                    f"30-day forecast: expected total revenue **{fc['summary']['total_forecast_revenue']:,.2f}** "
                    f"(avg daily **{fc['summary']['avg_daily_forecast']:,.2f}**). "
                    f"Trend direction: **{fc['summary']['trend_direction']}**."
                )
                response["metrics_used"] = ["forecast_30d"]
            else:
                response["answer"] = fc.get("error", "Forecast unavailable.")
        else:
            response["answer"] = "Forecasting requires order_date field."
    
    elif "churn" in question or "risk" in question:
        if "customer_id" in df.columns:
            churn = ChurnPredictor(df).train_and_predict()
            response["answer"] = (
                f"Churn analysis complete. Overall churn rate: **{churn.get('churn_rate', 0)*100:.1f}%**. "
                f"Risk distribution: {churn.get('risk_distribution', {})}. "
                f"Method: {churn.get('method')}."
            )
            response["metrics_used"] = ["churn_rate", "risk_bands"]
        else:
            response["answer"] = "Churn prediction requires customer_id."
    
    else:
        response["answer"] = (
            f"I can help with revenue, customers, products, forecasting, and churn analysis. "
            f"Current snapshot: Revenue **{kpis['total_revenue']:,.2f}**, "
            f"**{kpis['total_orders']}** orders, **{kpis['unique_customers']}** customers."
        )
        response["metrics_used"] = list(kpis.keys())
    
    return response

@app.get("/api/v1/intelligence/{dataset_id}/modules")
async def available_modules(dataset_id: str):
    if dataset_id not in DATASETS:
        raise HTTPException(404, "Dataset not found")
    return {
        "available_modules": DATASETS[dataset_id]["available_modules"],
        "data_health": DATASETS[dataset_id]["data_health"],
        "profile": DATASETS[dataset_id]["profile"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
