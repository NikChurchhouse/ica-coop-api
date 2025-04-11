from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class SpecialOffer(BaseModel):
    store: str
    product: str
    price: str
    valid_until: str

@app.get("/")
async def root():
    return {"message": "Hello! Use /specials/ica or /specials/coop to see offers."}

@app.get("/specials/ica", response_model=list[SpecialOffer])
async def get_ica_specials():
    url = "https://www.ica.se/erbjudanden/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    offers = []
    for item in soup.select(".offer-card__body"):
        product = item.select_one(".offer-card__name")
        price = item.select_one(".offer-card__price")
        valid_until = "unbekannt"  # ICA zeigt manchmal kein Enddatum direkt an

        if product and price:
            offers.append(SpecialOffer(
                store="ICA",
                product=product.get_text(strip=True),
                price=price.get_text(strip=True),
                valid_until=valid_until
            ))

    return offers

@app.get("/specials/coop", response_model=list[SpecialOffer])
async def get_coop_specials():
    url = "https://www.coop.se/handla/erbjudanden/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    offers = []
    for item in soup.select(".product-card"):
        product = item.select_one(".product-card-title")
        price = item.select_one(".product-card-price")
        valid_until = "unbekannt"  # Coop zeigt manchmal kein Enddatum direkt an

        if product and price:
            offers.append(SpecialOffer(
                store="Coop",
                product=product.get_text(strip=True),
                price=price.get_text(strip=True),
                valid_until=valid_until
            ))

    return offers
