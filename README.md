# Task 2: Sentiment and Thematic Analysis

## Overview
This notebook performs sentiment and thematic analysis on mobile banking app reviews from Ethiopian banks (CBE, BOA, Dashen Bank). The goal is to quantify user sentiment and uncover key themes to understand satisfaction drivers and pain points.

## Dataset
- **File:** `clean_reviews.csv`
- **Columns:**
  - `review_text`: Text of the review
  - `rating`: Star rating of the review (1-5)
  - `review_date`: Date of the review
  - `bank`: Name of the bank
  - `source`: Source of the review (Google Play Store, etc.)

## Workflow
1. **Preprocessing**
   - Lowercasing
   - Optional: stopword removal, lemmatization
2. **Sentiment Analysis**
   - **TextBlob**: Lexicon-based polarity and subjectivity
   - **VADER**: Compound sentiment scores and labels
   - Aggregation of sentiment by bank
3. **Thematic Analysis**
   - TF-IDF extraction of keywords
   - Grouping keywords into themes:
     - UI/UX Experience
     - Performance & Reliability
