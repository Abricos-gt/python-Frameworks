 # ============================================================
# Part 1: Data Loading and Basic Exploration
# ============================================================

# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re

# 1. Load the dataset
df = pd.read_csv('metadata.readme')

# 2. Display first few rows
print("Sample data:")
print(df.head())

# 3. Check basic info
print("\nDataFrame Info:")
print(df.info())

# 4. Check shape (rows, columns)
print("\nShape of dataset:", df.shape)

# 5. Check missing values
print("\nMissing values per column:")
print(df.isnull().sum().head(10))

# 6. Basic statistics
print("\nSummary statistics for numeric columns:")
print(df.describe())


# ============================================================
# Part 2: Data Cleaning and Preparation
# ============================================================

# Handle missing values
print("\nCleaning data...")

# Remove rows with no title, abstract, or publication date
df_clean = df.dropna(subset=['title', 'abstract', 'publish_time'])

# Fill missing journal names with 'Unknown'
df_clean['journal'] = df_clean['journal'].fillna('Unknown')

# Convert publish_time to datetime
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Extract year from publish_time
df_clean['year'] = df_clean['publish_time'].dt.year

# Create new column: abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))

print("\nAfter cleaning, dataset shape:", df_clean.shape)
print(df_clean[['publish_time', 'year', 'abstract_word_count']].head())


# ============================================================
# Part 3: Data Analysis and Visualization
# ============================================================

# --- Analysis 1: Publications by year ---
year_counts = df_clean['year'].value_counts().sort_index()

# --- Analysis 2: Top journals ---
top_journals = df_clean['journal'].value_counts().head(10)

# --- Analysis 3: Most frequent words in titles ---
titles = ' '.join(df_clean['title'].dropna()).lower()
words = re.findall(r'\b[a-z]{4,}\b', titles)
word_freq = Counter(words)
common_words = word_freq.most_common(15)

print("\nMost common words in titles:")
print(common_words)


# --- Visualization 1: Publications over time ---
plt.figure(figsize=(8, 4))
sns.barplot(x=year_counts.index, y=year_counts.values)
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.tight_layout()
plt.show()

# --- Visualization 2: Top Journals ---
plt.figure(figsize=(8, 4))
sns.barplot(y=top_journals.index, x=top_journals.values)
plt.title("Top Journals Publishing COVID-19 Research")
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
plt.tight_layout()
plt.show()

# --- Visualization 3: Word Cloud for Paper Titles ---
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df_clean['title'].dropna()))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of Paper Titles")
plt.show()


# ============================================================
# Part 4: Streamlit Application
# ============================================================

# Save a simplified version for Streamlit
df_clean.to_csv('data/metadata_clean.csv', index=False)

print("\nCleaned data saved for Streamlit app -> data/metadata_clean.csv")
