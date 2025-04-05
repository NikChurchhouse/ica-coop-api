from fastapi import FastAPI
from typing import List

app = FastAPI()

offers_data = {
    "ica": [
        {"name": "Milch 1L", "price": 10, "discount": "10%"},
        {"name": "Brot", "price": 15, "discount": "15%"},
    ],
    "coop": [
        {"name": "Käse 200g", "price": 25, "discount": "20%"},
        {"name": "Äpfel 1kg", "price": 30, "discount": "5%"},
    ]
}

@app.get("/")
def read_root():
    return {"message": "ICA & Coop Offers API"}

@app.get("/offers/{store}", response_model=List[dict])
def get_offers(store: str):
    store = store.lower()
    return offers_data.get(store, [])
