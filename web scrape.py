import requests
from bs4 import BeautifulSoup
import csv

# Define the base URL and headers
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
headers = {
    "User-Agent": "use your user agent to bypass"
}

# Part 1: Scraping Product Listings
with open("amazon_products.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"])

    for page_number in range(1, 21):  # Scraping 20 pages
        params = {
            "k": "bags",
            "crid": "2M096C61O4MLT",
            "qid": "1653308124",
            "sprefix": "ba,aps,283",
            "ref": f"sr_pg_{page_number}",
        }
        response = requests.get(base_url, headers=headers, params=params)
        
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
        
        for product in products:
            product_url = product.find("a", class_="a-link-normal").get("href")
            product_name = product.find("span", class_="a-text-normal").text
            product_price = product.find("span", class_="a-price-whole").text
            rating = product.find("span", class_="a-icon-alt").text
            num_reviews = product.find("span", class_="a-size-base").text.split()[0]
            
            csv_writer.writerow([product_url, product_name, product_price, rating, num_reviews])

            
print(response.content)

# Part 2: Scraping Additional Product Information
product_urls = []
with open("amazon_products.csv", "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        product_urls.append(row[0])  # Product URL is in the first column

with open("amazon_products_additional.csv", "w", newline="", encoding="utf-8") as csv_file_additional:
    csv_writer_additional = csv.writer(csv_file_additional)
    csv_writer_additional.writerow(["Product URL", "Description", "ASIN", "Product Description", "Manufacturer"])

    for product_url in product_urls:
        response = requests.get(product_url, headers=headers)
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract information from the product page and add to the CSV
        description = soup.find("meta", {"name": "description"}).get("content", "")
        asin = soup.find("th", text="ASIN").find_next_sibling("td").text.strip()
        product_desc = soup.find("div", {"id": "productDescription"}).text.strip()
        manufacturer = soup.find("a", {"id": "bylineInfo"}).text.strip()
        
        csv_writer_additional.writerow([product_url, description, asin, product_desc, manufacturer])


      
