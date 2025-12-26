import requests
from bs4 import BeautifulSoup
from scraper.utils import parse_date_safe, safe_text

BASE_URL = "https://www.g2.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_g2_reviews(company, start_date, end_date):
    page = 1
    results = []

    while True:
        url = f"{BASE_URL}/products/{company}/reviews?page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        reviews = soup.find_all("div", class_="paper")

        if not reviews:
            break

        for r in reviews:
            date_el = r.find("time")
            date = parse_date_safe(date_el["datetime"]) if date_el else None

            if not date or date < start_date:
                return results

            if start_date <= date <= end_date:
                results.append({
                    "title": safe_text(r.find("h3")),
                    "review": safe_text(r.find("div", class_="formatted-text")),
                    "date": date.isoformat(),
                    "rating": safe_text(r.find("span", class_="star-rating")),
                    "reviewer": safe_text(r.find("div", class_="user-name")),
                    "source": "G2"
                })
        page += 1

    return results
