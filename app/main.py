from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import Base, engine, get_db
from . import models, crud, recommender, schemas

app = FastAPI(
    title="FastAPI AI Recommendation Backend",
    description="구매 이력을 기반으로 AI 추천을 제공하는 예제 백엔드",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 테이블 생성 (운영 환경에서는 별도 마이그레이션 도구 사용 권장)
Base.metadata.create_all(bind=engine)

@app.get("/api/products", response_model=List[schemas.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    products = crud.get_all_products(db)
    return products

@app.get("/api/recommendations/{user_id}", response_model=List[schemas.RecommendationResponse])
def recommend(user_id: int, db: Session = Depends(get_db)):
    triples = crud.get_user_purchase_matrix(db)
    ranked = recommender.recommend_for_user(user_id, triples, top_k=5)
    if not ranked:
        raise HTTPException(status_code=404, detail="해당 사용자 구매 이력이 없습니다.")

    product_ids = [pid for pid, score in ranked]
    products = {p.id: p for p in crud.get_products_by_ids(db, product_ids)}

    result = []
    for pid, score in ranked:
        prod = products.get(pid)
        if not prod:
            continue
        result.append(
            schemas.RecommendationResponse(
                id=prod.id,
                name=prod.name,
                category=prod.category,
                price=prod.price,
                score=float(round(score, 4)),
            )
        )
    return result

@app.get("/")
def root():
    return {"message": "FastAPI recommendation backend is running"}

@app.get("/api/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "FastAPI Backend",
        "version": "0.1.0"
    }
