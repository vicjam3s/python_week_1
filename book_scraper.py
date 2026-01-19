import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

BOOKS_URL = "https://books.toscrape.com/"

print("Starting book scraper...")

try:
    
    response = requests.get(BOOKS_URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    book_tags = soup.select("article.product_pod")[:10]

    books = []

    for book in book_tags:
        title = book.h3.a["title"]
        price_text = book.select_one(".price_color").text.strip()

        books.append({
            "title": title,
            "price": price_text
        })

    if not books:
        raise Exception("No books found.")

    
    df = pd.DataFrame(books)
    print("\nBook Prices (Original Currency):\n")
    print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))

  
    df.to_csv("books.csv", index=False)
    df.to_json("books.json", orient="records", indent=4)

    print("\nSaved to books.csv and books.json")

except requests.exceptions.RequestException as e:
    print("[ERROR] Network error:", e)

except Exception as e:
    print("[ERROR] Something went wrong:", e)
