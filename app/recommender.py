"""
매우 단순한 아이템 기반 추천 예제입니다.

- 사용자-상품 구매 행렬을 받아서
- 상품 간 co-occurrence(같이 구매된 횟수)를 기준으로 유사도 점수 계산
- 특정 user_id의 과거 구매 상품을 기준으로 상위 N개 상품 추천
"""
from collections import defaultdict
from typing import List, Tuple

def build_item_cooccurrence(purchase_triples: List[Tuple[int, int, int]]):
    # purchase_triples: (user_id, product_id, qty)
    user_to_items = defaultdict(list)
    for user_id, product_id, qty in purchase_triples:
        user_to_items[user_id].append((product_id, qty))

    co_counts = defaultdict(lambda: defaultdict(float))
    item_counts = defaultdict(float)

    for user_id, items in user_to_items.items():
        product_ids = []
        for pid, qty in items:
            product_ids.extend([pid] * int(qty))
        unique = set(product_ids)
        for i in unique:
            item_counts[i] += 1.0
        for i in unique:
            for j in unique:
                if i == j:
                    continue
                co_counts[i][j] += 1.0

    item_sim = defaultdict(dict)
    for i, related in co_counts.items():
        for j, cij in related.items():
            denom = (item_counts[i] * item_counts[j]) ** 0.5
            if denom > 0:
                item_sim[i][j] = cij / denom

    return item_sim

def recommend_for_user(user_id: int, purchase_triples: List[Tuple[int, int, int]], top_k: int = 5):
    user_items = defaultdict(int)
    for uid, pid, qty in purchase_triples:
        if uid == user_id:
            user_items[pid] += int(qty)

    if not user_items:
        return []

    item_sim = build_item_cooccurrence(purchase_triples)

    scores = defaultdict(float)
    for owned_pid, owned_qty in user_items.items():
        similar_dict = item_sim.get(owned_pid, {})
        for other_pid, sim in similar_dict.items():
            if other_pid in user_items:
                continue
            scores[other_pid] += sim * owned_qty

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
