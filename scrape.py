import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import json
import csv

BOOKS_URL = "https://books.toscrape.com/"
RATE_API = "https://open.er-api.com/v6/latest/GBP"
TARGET_CURRENCY = "KES"   # change to USD, EUR, etc.

print("Starting scraper...")

try:
    # 1. Get books page
    response = requests.get(BOOKS_URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    book_tags = soup.select("article.product_pod")[:10]

    books = []

    for book in book_tags:
        title = book.h3.a["title"]
        price_text = book.select_one(".price_color").text
        price_gbp = float(price_text.replace("£", ""))

        books.append({
            "title": title,
            "price_gbp": price_gbp
        })

    # 2. Get exchange rate
    rate_response = requests.get(RATE_API, timeout=10)
    rate_response.raise_for_status()
    rate_data = rate_response.json()

    rate = rate_data["rates"][TARGET_CURRENCY]

    # 3. Convert prices
    for book in books:
        book[f"price_{TARGET_CURRENCY.lower()}"] = round(book["price_gbp"] * rate, 2)

    # 4. Display table
    df = pd.DataFrame(books)
    print("\nConverted Prices:\n")
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))

    # 5. Save files
    df.to_csv("books.csv", index=False)
    df.to_json("books.json", orient="records", indent=4)

    print("\nSaved to books.csv and books.json")

except requests.exceptions.RequestException as e:
    print("[ERROR] Network error:", e)

except Exception as e:
    print("[ERROR] Something went wrong:", e)

