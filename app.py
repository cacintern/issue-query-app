import streamlit as st
import openai
import pandas as pd
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Issue Query App", layout="wide")

# Custom header in Citizen Advocacy Center colors
st.markdown(
    """
    <style>
        .main-header {
            background-color: #FFD700;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }
        .main-header h2 {
            color: #0033A0;
        }
        .stSlider > div {
            color: #0033A0;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            font-size: 16px;
            color: #0033A0;
        }
        .footer strong {
            color: #FFD700;
        }
        .stButton>button {
            background-color: #0033A0;
            color: white;
            border-radius: 5px;
            padding: 0.5em 1em;
            border: none;
        }
        .stButton>button:hover {
            background-color: #002270;
        }
        .stSlider .st-cf {
            color: #0033A0 !important;
        }
    </style>
    <div class="main-header">
        <h2>📘 Welcome to the Issue Query App</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar API key entry
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

# Load and merge data on 'Issue'
df_Main = pd.read_csv("Main.csv")
df_County = pd.read_csv("County.csv")
df_Ambassadors = pd.read_csv("Ambassadors.csv")
df_City_Town = pd.read_csv("City_Town.csv")
df_Organizations_Coalitions = pd.read_csv("Organizations_Coalitions.csv")
df_Year = pd.read_csv("Year.csv")

df = df_Main
for other_df in [df_County, df_Ambassadors, df_City_Town, df_Organizations_Coalitions, df_Year]:
    df = pd.merge(df, other_df, on="Issue", how="left")

# Layout: header and download button side by side
header_col, button_col = st.columns([4, 1])  # Adjust ratios to fit your layout

with header_col:
    st.subheader("🧾 Preview of Your Merged Data")

with button_col:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='merged_data.csv',
        mime='text/csv',
        key="download-button"
    )

# User query input
user_query = st.text_input("🔍 Ask a question about your data (e.g. 'Show me issues with FOIA true in Elgin in 2019'):")

if user_query:
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

# Footer
st.markdown(
    """
    <div class="footer">
        Made with 💙 & 💛 by <strong>Citizen Advocacy Center</strong><br>
        <em>“Let's build democracy!”</em>
    </div>
    """,
    unsafe_allow_html=True
)
