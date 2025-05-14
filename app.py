import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="Issue Query Assistant", layout="wide")

st.title("🔎 Issue Query Assistant")
st.write("Ask questions about your issues database using natural language.")

openai_api_key = st.sidebar.text_input("🔑 Enter your OpenAI API Key", type="password")

uploaded_file = st.file_uploader("📁 Upload your CSV file", type="csv")

if uploaded_file and openai_api_key:
    df = pd.read_csv(uploaded_file)
    st.success("✅ CSV file loaded!")

    st.subheader("🧾 Sample Data")
    st.dataframe(df.head(10))

    query = st.text_input("💬 Ask a question about your data")

    if query:
        # Create a prompt for GPT
        sample_data = df.head(5).to_dict(orient="records")
        prompt = f"""You are a helpful assistant working with tabular data. The dataset columns are: {list(df.columns)}.
        Here are the first few rows:\n{sample_data}\n\n
        The user asked: "{query}"\n
        Interpret the question and return the matching rows as a markdown table."""

        openai.api_key = openai_api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        st.markdown(response.choices[0].message.content)

elif not uploaded_file:
    st.info("Upload a CSV file to get started.")
elif not openai_api_key:
    st.info("Enter your OpenAI API key in the sidebar.")
