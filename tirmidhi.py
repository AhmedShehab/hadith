import os
import streamlit as st
import pandas as pd
from llama_index.experimental.query_engine import PandasQueryEngine
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Check if the OpenAI API key is set
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    # Set the page title and header for the Streamlit app
    st.set_page_config(page_title="Tirmidhi Wiki")
    st.header("Ask a Question in Ahadith al Tirmidhi: ")

    # Allow user to upload a CSV file
    # csv_file = st.file_uploader("Upload a CSV file", type="csv")
    csv_file = "./tirmidhi.csv"

    if csv_file is not None:
        # Load the uploaded CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Replace NaN values in the DataFrame with the word 'empty'
        df.fillna("empty", inplace=True)

        # Save the modified DataFrame to a CSV file
        df.to_csv("tirmidhi_filled.csv", index=False)

        # Initialize the PandasQueryEngine for querying the DataFrame
        query_engine = PandasQueryEngine(df=df, verbose=True, synthesize_response=True)

        # Get a question from the user to query the CSV file
        user_question = st.text_input("Ask a question Ahadith al Tirmidhi: ")

        if user_question is not None and user_question != "":
            # Show a spinner while processing
            with st.spinner(text="In progress..."):  
                # Query the DataFrame using user input
                query = query_engine.query(user_question)  
                # Display the query result
                st.write(query.response)


if __name__ == "__main__":
    main()
