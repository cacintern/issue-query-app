import streamlit as st
import openai
import pandas as pd
import os

# Set page title
st.set_page_config(page_title="Issue Query App", layout="wide")
st.title("📂 Issue Query App")

# Sidebar for OpenAI API Key
openai_api_key = st.sidebar.text_input("🔑 Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to begin.")
    st.stop()

openai.api_key = openai_api_key

# Upload or load CSV data
df = pd.read_csv("Main.csv")  # replace with the exact name of your file
df_Main = pd.read_csv("Main.csv")
df_County = pd.read_csv("County.csv")
df_Ambassadors = pd.read_csv("Ambassadors.csv")
df_City_Town = pd.read_csv("City_Town.csv")
df_Organizations_Coalitions = pd.read_csv("Organizations_Coalitions.csv")
df_Year = pd.read_csv("Year.csv")

st.subheader("Preview of Your Data")
st.dataframe(df.head(20))

user_query = st.text_input("🔍 Ask a question about your data (e.g. 'Show me issues in Elgin in 2019 where TIF is true'):")

if user_query:
        # Send user question + sample data to OpenAI
        prompt = f"""You are a data assistant. Based on the following table, answer the user's question.

User's question: {user_query}

Here are the first few rows of the data:
{df.head(15).to_csv(index=False)}

Give a clear, helpful answer using the table above. If the answer isn't obvious, explain what you'd need.
"""

        try:
            with st.spinner("Thinking..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0,
                )
                st.success("Answer:")
                st.write(response['choices'][0]['message']['content'])
        except Exception as e:
            st.error(f"❌ OpenAI error: {e}")
else:
    st.info("Upload a CSV file from your Access database export to get started.")
