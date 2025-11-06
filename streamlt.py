import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")

# Title and intro
st.title("📊 CORD-19 Data Explorer")
st.write("""
This app provides a simple interactive exploration of COVID-19 research papers
based on the **CORD-19 metadata** dataset.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/metadata_clean.csv')
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
min_year, max_year = int(df['year'].min()), int(df['year'].max())
year_range = st.sidebar.slider("Select publication year range", min_year, max_year, (2020, 2021))

filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Publications by year
st.subheader("📅 Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
sns.barplot(x=year_counts.index, y=year_counts.values, ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Top Journals
st.subheader("🏛️ Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax)
ax.set_xlabel("Number of Papers")
ax.set_ylabel("Journal")
st.pyplot(fig)

# Show data sample
st.subheader("📄 Sample of Data")
st.dataframe(filtered.head())
