import os
import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient("meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN)


st.set_page_config(page_title="AI Currency Converter")
st.title("AI Currency Converter")


with st.form(key='converter_form'):
    amount = st.text_input("Amount", value="1")
    from_curr = st.text_input("From Currency (e.g. USD)", value="USD")
    to_curr = st.text_input("To Currency (e.g. EUR)", value="EUR")
    
    submit_button = st.form_submit_button(label='Convert')

# CONVERSION LOGIC 
if submit_button:
    if amount and from_curr and to_curr:
        # The Prompt for Llama
        prompt = (
            f"Convert {amount} {from_curr} to {to_curr}. "
            "Use current approximate market rates. Provide only the final converted amount "
            "and a very short explanation."
        )

        with st.spinner("AI is calculating rates..."):
            try:
                # 3. AI Chat Completion
                response = client.chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=100,
                    temperature=0.1
                )
                
                # Extracting the content
                result = response.choices[0].message.content
                
                # Display Result 
                st.success("### Conversion Result")
                st.write(result)
                
            except Exception as e:
                st.error(f"Error: {str(e)}. Please check your connection or API key.")
    else:
        st.warning("Please fill in all fields.")