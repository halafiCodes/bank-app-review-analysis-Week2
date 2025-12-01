
# 📦 Task 3 — Store Cleaned Review Data in PostgreSQL

This task is part of the **Mobile Banking Review Analytics Project**.
The goal is to create a PostgreSQL database, define a schema, and insert cleaned and processed review data from CSV files.

---

## ✅ **1. Overview**

In Task 3, we store the cleaned Google Play Store reviews for Ethiopian banks in a PostgreSQL database. This allows efficient querying, aggregation, and integration with future analytics dashboards.

Banks included:

* **Commercial Bank of Ethiopia (CBE)**
* **Bank of Abyssinia (BOA)**
* **Dashen Bank**

Each review contains the reviewer’s message, rating, date, bank name, sentiment label and score.

---

## 🗄️ **2. Database Schema**

This project uses **two tables**: `banks` and `reviews`.

### **📌 banks Table**

Stores basic information about each bank.

| Column    | Type         | Description            |
| --------- | ------------ | ---------------------- |
| bank_id   | SERIAL (PK)  | Unique ID per bank     |
| bank_name | VARCHAR(100) | Name of the bank       |
| app_name  | VARCHAR(150) | Mobile app name / code |

---

### **📌 reviews Table**

Stores individual review information.

| Column          | Type        | Description                   |
| --------------- | ----------- | ----------------------------- |
| review_id       | SERIAL (PK) | Unique ID per review          |
| bank_id         | INT (FK)    | References `banks.bank_id`    |
| review_text     | TEXT        | The review message            |
| rating          | INT         | Numeric rating (1–5)          |
| review_date     | DATE        | Date of review                |
| sentiment_label | VARCHAR(20) | Positive / Negative / Neutral |
| sentiment_score | FLOAT       | Sentiment confidence score    |
| source          | VARCHAR(50) | Source (Google Play)          |

---

## ⚙️ **3. SQL Setup**

Run the following in **pgAdmin** or `psql`:

```sql
-- Banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100),
    app_name VARCHAR(150)
);

-- Reviews table
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT,
    rating INT,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    source VARCHAR(50)
);

-- Insert banks
INSERT INTO banks (bank_name, app_name)
VALUES
('Commercial Bank of Ethiopia', 'CBE'),
('Bank of Abyssinia', 'BOA'),
('Dashen Bank', 'DB');
```

---

## 🐍 **4. Insert Reviews Using Python**

The script **`scripts/insert_reviews.py`** reads cleaned CSV files and inserts them into PostgreSQL.

### **Run the script:**

```bash
python scripts/insert_reviews.py
```

Expected output:

```
['CBE' 'BOA' 'Dashen']
Reviews inserted successfully!
```

---

## 📊 **5. Verification Queries**

### **Check number of records:**

```sql
SELECT COUNT(*) FROM reviews;
```

### **Check all banks appear correctly:**

```sql
SELECT b.bank_name, COUNT(r.review_id) AS total_reviews
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;
```

```
Bank of Abyssinia | 334
Commercial Bank of Ethiopia | 324
Dashen Bank | 171
```

```






