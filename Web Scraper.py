import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin


# ---------------------------------------
# Settings
# ---------------------------------------

BASE_URL = "https://books.toscrape.com/"
START_URL = BASE_URL + "catalogue/page-1.html"
OUTPUT_FILE = "books.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


# ---------------------------------------
# Get page HTML
# ---------------------------------------

def get_page(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.text

    except requests.exceptions.Timeout:
        print("Request timed out:", url)

    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)

    except requests.exceptions.RequestException as error:
        print("Request error:", error)

    return None


# ---------------------------------------
# Convert rating text to number
# ---------------------------------------

def get_rating(rating_text):

    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    return ratings.get(rating_text, "N/A")


# ---------------------------------------
# Scrape one page
# ---------------------------------------

def scrape_page(url):

    html = get_page(url)

    if html is None:
        return []

    soup = BeautifulSoup(html, "html.parser")

    books = []

    book_items = soup.select("article.product_pod")

    for book in book_items:

        # Title
        title_tag = book.select_one("h3 a")

        if title_tag:
            title = title_tag.get("title", "N/A")
        else:
            title = "N/A"

        # Price
        price_tag = book.select_one(".price_color")

        if price_tag:
            price = price_tag.get_text(strip=True)
        else:
            price = "N/A"

        # Rating
        rating_tag = book.select_one(".star-rating")

        if rating_tag:
            rating_class = rating_tag.get("class", [])

            if len(rating_class) > 1:
                rating = get_rating(rating_class[1])
            else:
                rating = "N/A"
        else:
            rating = "N/A"

        # Availability
        availability_tag = book.select_one(".availability")

        if availability_tag:
            availability = availability_tag.get_text(
                strip=True
            )
        else:
            availability = "N/A"

        # Book URL
        if title_tag:
            relative_url = title_tag.get("href")
            book_url = urljoin(url, relative_url)
        else:
            book_url = "N/A"

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": book_url
        })

    return books


# ---------------------------------------
# Find next page
# ---------------------------------------

def get_next_page(url):

    html = get_page(url)

    if html is None:
        return None

    soup = BeautifulSoup(html, "html.parser")

    next_button = soup.select_one("li.next a")

    if next_button:

        next_url = next_button.get("href")

        return urljoin(url, next_url)

    return None


# ---------------------------------------
# Save data to CSV
# ---------------------------------------

def save_to_csv(books):

    if not books:
        print("No data found.")
        return

    fieldnames = [
        "title",
        "price",
        "rating",
        "availability",
        "url"
    ]

    try:

        with open(
            OUTPUT_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(books)

        print("\nData saved successfully!")
        print("Output file:", OUTPUT_FILE)

    except OSError as error:
        print("Error saving CSV:", error)


# ---------------------------------------
# Main Scraper
# ---------------------------------------

def main():

    print("=" * 50)
    print("          BOOKS WEB SCRAPER")
    print("=" * 50)

    all_books = []

    current_url = START_URL

    page_number = 1

    # Scrape at least two pages
    MAX_PAGES = 3

    while current_url and page_number <= MAX_PAGES:

        print(f"\nScraping page {page_number}...")
        print(current_url)

        books = scrape_page(current_url)

        if books:

            all_books.extend(books)

            print(
                f"Found {len(books)} books."
            )

        else:

            print("No books found on this page.")

        # Stop if maximum pages reached
        if page_number >= MAX_PAGES:
            break

        # Find next page
        current_url = get_next_page(current_url)

        page_number += 1

        # Delay between requests
        time.sleep(2)

    # Save results
    save_to_csv(all_books)

    # Summary
    print("\n" + "=" * 50)
    print("SCRAPING COMPLETED")
    print("=" * 50)

    print("Pages scraped :", page_number)
    print("Books scraped :", len(all_books))
    print("CSV file      :", OUTPUT_FILE)


# ---------------------------------------
# Run program
# ---------------------------------------

if __name__ == "__main__":
    main()