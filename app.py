import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# Streamlit page setup
st.set_page_config(page_title="Issue Query App", layout="wide")
st.title("📂 Issue Query App")

# Sidebar API Key
openai_api_key = st.sidebar.text_input("🔑 Enter your OpenAI API Key", type="password")
if not openai_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to begin.")
    st.stop()

# Load all CSVs
df_main = pd.read_csv("Main.csv")
df_county = pd.read_csv("County.csv")
df_ambassadors = pd.read_csv("Ambassadors.csv")
df_city = pd.read_csv("City_Town.csv")
df_orgs = pd.read_csv("Organizations_Coalitions.csv")
df_year = pd.read_csv("Year.csv")

# Merge them on the shared "Issue" column
df = df_main.copy()
dfs_to_merge = [df_county, df_ambassadors, df_city, df_orgs, df_year]
for sub_df in dfs_to_merge:
    if "Issue" in sub_df.columns:
        df = pd.merge(df, sub_df, on="Issue", how="left")

# Preview the merged dataset
st.subheader("🧾 CAC Annual Report Merged Data")
num_rows = st.slider("How many rows to preview?", min_value=5, max_value=len(df), value=20, step=5)
st.dataframe(
    df.head(num_rows),
    use_container_width=True,
    hide_index=False,
    column_order=("Issue", *[col for col in df.columns if col != "Issue"]),
)

# Get user's question
user_query = st.text_input("🔍 Ask a question about your data (e.g. 'Show me issues in Elgin in 2019 where TIF is true'):")

# Only continue if query is entered
if user_query:
    # Create prompt with a sample of the merged data
    prompt = f"""You are a helpful data assistant. Use the table below to answer the user's question.

User's question: {user_query}

Here are a few rows from the dataset:
{df.head(15).to_csv(index=False)}

⚠️ Only show a list of relevant issues from the 'Issue' column, unless the user asks for more details or other columns. Avoid repeating all columns unless requested.

Respond clearly using only the data. If something is unclear, say what info is missing.
"""

    try:
        with st.spinner("Thinking..."):
            client = OpenAI(api_key=openai_api_key)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes CSV data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
            )

            st.success("Answer:")
            st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"❌ OpenAI error: {e}")
else:
    st.info("Enter a question to analyze the data.")
