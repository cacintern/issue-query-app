import streamlit as st
import openai
import pandas as pd
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Issue Query App", layout="wide")

# Custom blue and yellow banner
st.markdown(
    """
    <div style='background-color:#FFD700; padding: 10px; border-radius: 8px; text-align:center; margin-bottom:20px'>
        <h2 style='color:#0033A0;'>📘 Welcome to the Issue Query App</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar with styled prompt for API key
st.sidebar.markdown(
    """
    <div style='background-color:#0033A0; padding:10px; border-radius:5px'>
        <h3 style='color:#FFD700;'>🔑 Enter Your OpenAI Key</h3>
    </div>
    """,
    unsafe_allow_html=True
)
openai_api_key = st.sidebar.text_input("API Key", type="password")

if not openai_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to begin.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# Load all CSVs and merge on 'Issue'
df_Main = pd.read_csv("Main.csv")
df_County = pd.read_csv("County.csv")
df_Ambassadors = pd.read_csv("Ambassadors.csv")
df_City_Town = pd.read_csv("City_Town.csv")
df_Organizations_Coalitions = pd.read_csv("Organizations_Coalitions.csv")
df_Year = pd.read_csv("Year.csv")

# Merge all on 'Issue'
df = df_Main
for other_df in [df_County, df_Ambassadors, df_City_Town, df_Organizations_Coalitions, df_Year]:
    df = pd.merge(df, other_df, on="Issue", how="left")

# Preview merged dataset
st.subheader("🧾 Preview of Your Merged Data")
num_rows = st.slider("How many rows to preview?", min_value=5, max_value=len(df), value=100, step=5)
st.dataframe(df.head(num_rows))

# Text input for user query
user_query = st.text_input("🔍 Ask a question about your data (e.g. 'Show me issues with FOIA true in Elgin in 2019'):")

if user_query:
    # Prompt to OpenAI
    prompt = f"""You are a helpful data assistant. Use the table below to answer the user's question.

User's question: {user_query}

Here are a few rows from the dataset:
{df.head(15).to_csv(index=False)}

⚠️ Only show a list of relevant issues from the 'Issue' column, unless the user asks for more details or other columns. Avoid repeating all columns unless requested.
"""

    try:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes CSV data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
            )
            st.success("✅ Answer:")
            st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"❌ OpenAI error: {e}")
