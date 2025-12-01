import psycopg2
import pandas as pd

df = pd.read_csv("data/clean_reviews_with_tb_sentiment.csv")

bank_mapping = {
    "CBE": 1,
    "BOA": 2,
    "Dashen": 3, 
}



df["bank_id"] = df["bank"].map(bank_mapping)

conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",  
    user="postgres",          
    password="1234",        
    port=5432
)

cur = conn.cursor()
df["bank_id"] = df["bank"].map(bank_mapping)
df = df.dropna(subset=["bank_id"])
df["bank_id"] = df["bank_id"].astype(int)


for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row["bank_id"]),          
        str(row["clean_text"]),     
        int(row["rating"]),           
        row["review_date"],           
        str(row["tb_sentiment"]),      
        float(row["tb_polarity"]),     
        str(row["source"])             
    ))


conn.commit()
cur.close()
conn.close()

print("Reviews inserted successfully!")
