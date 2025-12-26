import argparse
import json
from datetime import datetime
from scraper.utils import validate_date_range
from scraper.g2 import scrape_g2_reviews
from scraper.capterra import scrape_capterra_reviews
from scraper.trustradius import scrape_trustradius_reviews

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--source", required=True, choices=["g2", "capterra", "trustradius"])

    args = parser.parse_args()

    start_date = datetime.strptime(args.start, "%Y-%m-%d").date()
    end_date = datetime.strptime(args.end, "%Y-%m-%d").date()
    validate_date_range(start_date, end_date)

    if args.source == "g2":
        data = scrape_g2_reviews(args.company, start_date, end_date)
    elif args.source == "capterra":
        data = scrape_capterra_reviews(args.company, start_date, end_date)
    else:
        data = scrape_trustradius_reviews(args.company, start_date, end_date)

    filename = f"{args.company}_{args.source}_reviews.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ {len(data)} reviews saved to {filename}")

if __name__ == "__main__":
    main()
