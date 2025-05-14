import streamlit as st
import pandas as pd
from openai import OpenAI

# Set page title
st.set_page_config(page_title="Issue Query App", layout="wide")
st.title("📂 Issue Query App")

# Sidebar for OpenAI API Key
openai_api_key = st.sidebar.text_input("🔑 Enter your OpenAI API Key", type="password")

if not openai_api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to begin.")
    st.stop()

# Load your CSV data files (make sure these filenames match exactly)
df = pd.read_csv("Main.csv")
df_County = pd.read_csv("County.csv")
df_Ambassadors = pd.read_csv("Ambassadors.csv")
df_City_Town = pd.read_csv("City_Town.csv")
df_Organizations_Coalitions = pd.read_csv("Organizations_Coalitions.csv")
df_Year = pd.read_csv("Year.csv")

st.subheader("Preview of Your Main Data")
st.dataframe(df.head(20))

# Add a column description dictionary for GPT context
column_descriptions = """
- TIF: Whether the issue involves Tax Increment Financing (True/False)
- FOIA: Whether the issue relates to Freedom of Information Act requests (True/False)
- City: The city where the issue occurred
- Year: The year the issue took place
- Description: A short text description of the issue
- County: The county where the issue occurred
- Ambassador: Whether an ambassador is involved (True/False)
- Organization/Coalition: Related organizations or coalitions
- Other columns: (Add descriptions as needed)
"""

user_query = st.text_input("🔍 Ask a question about your data (e.g. 'Show me issues in Elgin in 2019 where TIF is true'):")

if user_query:
    # Prepare a structured sample of your data as a list of dicts for GPT
    sample_rows = df.head(15).to_dict(orient="records")

    prompt = f"""
You are a helpful data assistant. Use the following data to answer the user's question.

Column descriptions:
{column_descriptions}

User's question: {user_query}

Data sample:
{sample_rows}

Please provide a clear, helpful answer based on the data above. If the answer cannot be determined from this data, please explain what additional information is needed.
"""

    with st.spinner("Thinking..."):
        try:
            client = OpenAI(api_key=openai_api_key)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes data from CSV files."},
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
