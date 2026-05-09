import os
import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Hugging Face Client
client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)

# Streamlit Page Config
st.set_page_config(page_title="AI Currency Converter")

st.title("💱 AI Currency Converter")

# Currency List
currencies = [
    "USD",  # US Dollar
    "INR",  # Indian Rupee
    "EUR",  # Euro
    "GBP",  # British Pound
    "JPY",  # Japanese Yen
    "AUD",  # Australian Dollar
    "CAD",  # Canadian Dollar
    "CHF",  # Swiss Franc
    "CNY",  # Chinese Yuan
    "SGD"   # Singapore Dollar
]

# Form
with st.form(key='converter_form'):

    amount = st.number_input(
        "Enter Amount",
        min_value=1.0,
        value=1.0
    )

    from_curr = st.selectbox(
        "From Currency",
        currencies,
        index=0
    )

    to_curr = st.selectbox(
        "To Currency",
        currencies,
        index=1
    )

    submit_button = st.form_submit_button("Convert")

# Conversion Logic
if submit_button:

    if from_curr == to_curr:
        st.warning("Please select different currencies.")
    else:

        prompt = (
            f"Convert {amount} {from_curr} to {to_curr}. "
            "Use current approximate market exchange rates. "
            "Provide only the converted amount and a short explanation."
        )

        with st.spinner("AI is calculating exchange rates..."):

            try:
                response = client.chat_completion(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=100,
                    temperature=0.1
                )

                result = response.choices[0].message.content

                st.success("✅ Conversion Result")
                st.write(result)

            except Exception as e:
                st.error(
                    f"Error: {str(e)}\n"
                    "Please check your internet connection or API key."
                )