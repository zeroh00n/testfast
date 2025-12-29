from sqlalchemy.orm import Session
from . import models

def get_all_products(db: Session):
    return db.query(models.Product).order_by(models.Product.id).all()

def get_user_purchase_matrix(db: Session):
    """
    사용자-상품 구매 횟수 정보를 반환합니다.
    결과 예시: [(user_id, product_id, quantity), ...]
    """
    from sqlalchemy import func
    q = (
        db.query(
            models.Order.user_id,
            models.OrderItem.product_id,
            func.sum(models.OrderItem.quantity).label("qty"),
        )
        .join(models.OrderItem, models.Order.id == models.OrderItem.order_id)
        .group_by(models.Order.user_id, models.OrderItem.product_id)
    )
    return q.all()

def get_products_by_ids(db: Session, product_ids):
    return (
        db.query(models.Product)
        .filter(models.Product.id.in_(product_ids))
        .all()
    )
