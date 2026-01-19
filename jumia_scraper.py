# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from tabulate import tabulate

# JUMIA_URL = "https://www.jumia.co.ke/mlp-electronics/"
# RATE_API = "https://open.er-api.com/v6/latest/KES"
# TARGET_CURRENCY = "USD"


# print("Starting Jumia scraper...")

# try:
    
#     response = requests.get(JUMIA_URL)
#     response.raise_for_status()

#     soup = BeautifulSoup(response.text, "html.parser")
#     product_tags = soup.select("article.prd")[:10]

#     products = []

#     for product in product_tags:
#         name_tag = product.select_one("h3.name")
#         price_tag = product.select_one("div.prc")

#         name = name_tag.text.strip()
#         price_text = price_tag.text.strip()

#         price_kes = float(
#             price_text.replace("KSh", "")
#                       .replace(",", "")
#                       .strip()
#         )

#         products.append({
#             "product": name,
#             "price_kes": price_kes
#         })

#     if not products:
#         raise Exception("No products found. Jumia may be blocking the request.")

    
#     rate_response = requests.get(RATE_API, timeout=10)
#     rate_response.raise_for_status()
#     rate_data = rate_response.json()

#     rate = rate_data["rates"][TARGET_CURRENCY]


#     for item in products:
#         item[f"price_{TARGET_CURRENCY.lower()}"] = round(item["price_kes"] * rate, 2)

#     df = pd.DataFrame(products)
#     print("\nConverted Prices:\n")
#     print(tabulate(df, headers="keys", tablefmt="grid", showindex=False))


#     df.to_csv("jumia_products.csv", index=False)
#     df.to_json("jumia_products.json", orient="records", indent=4)

#     print("\nSaved to jumia_products.csv and jumia_products.json")

# except requests.exceptions.RequestException as e:
#     print("[ERROR] Network error:", e)

# except Exception as e:
#     print("[ERROR] Something went wrong:", e)
