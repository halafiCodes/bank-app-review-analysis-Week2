import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google_play_scraper import app, Sort, reviews
import pandas as pd
from datetime import datetime
import time
from tqdm import tqdm
from config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS


class PlayStoreScraper:
    def __init__(self):
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        self.reviews_per_bank = SCRAPING_CONFIG['reviews_per_bank']
        self.lang = SCRAPING_CONFIG['lang']
        self.country = SCRAPING_CONFIG['country']
        self.max_retries = SCRAPING_CONFIG['max_retries']

    def scrape_reviews(self, app_id, count=400):
        for attempt in range(self.max_retries):
            try:
                result, _ = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=count
                )
                return result
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(5)
                else:
                    return []

    def process_reviews(self, reviews_data, bank_code):
        processed = []
        for review in reviews_data:
            processed.append({
                'review_id': review.get('reviewId', ''),
                'review_text': review.get('content', ''),
                'rating': review.get('score', 0),
                'review_date': review.get('at', datetime.now()),
                'bank_code': bank_code,
                'bank_name': self.bank_names[bank_code],
                'source': 'Google Play'
            })
        return processed

    def scrape_all_banks(self):
        all_reviews = []

        for bank_code, app_id in tqdm(self.app_ids.items(), desc="Scraping Banks"):
            reviews_data = self.scrape_reviews(app_id, self.reviews_per_bank)
            if reviews_data:
                processed = self.process_reviews(reviews_data, bank_code)
                all_reviews.extend(processed)

        df = pd.DataFrame(all_reviews)

        # --- Preprocessing ---
        df = df.drop_duplicates(subset=['review_text'])
        df = df.dropna(subset=['review_text', 'rating', 'review_date'])
        df['review_date'] = pd.to_datetime(df['review_date']).dt.date
        df = df[['review_text', 'rating', 'review_date', 'bank_name', 'source']]
        df.columns = ['review', 'rating', 'date', 'bank', 'source']

        # Save cleaned CSV
        os.makedirs(DATA_PATHS['clean'], exist_ok=True)
        clean_path = os.path.join(DATA_PATHS['clean'], 'cleaned_reviews.csv')
        df.to_csv(clean_path, index=False)

        print(f"\nScraping + Preprocessing Complete! Saved to {clean_path}")
        return df


def main():
    scraper = PlayStoreScraper()
    df = scraper.scrape_all_banks()
    print(f"Total reviews after preprocessing: {len(df)}")
    return df


if __name__ == "__main__":
    reviews_df = main()
