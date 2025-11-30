import pandas as pd

def preprocess():
    df = pd.read_csv("../data/raw_reviews.csv")

    # Check if required columns exist
    required_cols = ['review_text', 'rating', 'review_date']
    for col in required_cols:
        if col not in df.columns:
            print(f"Column {col} not found in raw_reviews.csv!")
            return

    df = df.drop_duplicates(subset='review_text')
    df = df.dropna(subset=['review_text', 'rating', 'review_date'])
    df['review_date'] = pd.to_datetime(df['review_date']).dt.date
    df['review_text'] = df['review_text'].str.lower().str.strip()

    df.to_csv("../data/clean_reviews.csv", index=False)
    print("Preprocessing complete! Saved to data/clean_reviews.csv")

if __name__ == "__main__":
    preprocess()
