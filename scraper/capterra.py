import requests
from bs4 import BeautifulSoup
from scraper.utils import parse_date_safe, safe_text

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_capterra_reviews(company, start_date, end_date):
    url = f"https://www.capterra.com/p/{company}/reviews/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="review")

    results = []

    for c in cards:
        date = parse_date_safe(safe_text(c.find("time")))

        if not date or not (start_date <= date <= end_date):
            continue

        results.append({
            "title": safe_text(c.find("h3")),
            "review": safe_text(c.find("p")),
            "date": date.isoformat(),
            "rating": safe_text(c.find("span", class_="rating")),
            "reviewer": safe_text(c.find("span", class_="reviewer-name")),
            "source": "Capterra"
        })

    return results
