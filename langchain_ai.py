from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import json
import pandas as pd

# Set OpenAI API key
api_key = "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"

openai_llm = ChatOpenAI(temperature=0.3, openai_api_key=api_key, model="gpt-3.5-turbo")

# Define the prompt template
my_prompt_template_contract_info = PromptTemplate(
    input_variables=["contract_text"],
    template=(
        "You are an AI assistant  at Koyeb that extracts structured information from legal and partners contractual documents. "
        "Your task is to read the provided contract text and extract the following details:\n"
        "Contract Counterpart: The party or entity entering the contract.Not Koyeb\n"
        "Signing Date: The date the contract was signed.\n"
        "Due Date: The deadline or due date for any obligations.\n"
        "Price: The monetary value or compensation stated in the contract.\n"
        "Prestation Summary: A brief summary of the services or goods described in the contract.\n"
        "Is the contract valid: Does the contract contain a Bonnes pratiques clause ? Yes/No\n"
        "If any piece of information is missing or unclear, return 'NA' for that field.\n\n"
        "Input Contract:\n"
        "{contract_text}\n\n"
        "Output JSON Format:\n"
        "\n"
        '    "contract_counterpart": "Extracted Value or NA",\n'
        '    "signing_date": "Extracted Value or NA",\n'
        '    "due_date": "Extracted Value or NA",\n'
        '    "price": "Extracted Value or NA",\n'
        '    "prestation_summary": "Extracted Value or NA",\n'
        '    "contract_valid": "Yes/No"\n'
        "\n\n"
        "Make sure to output only the JSON, and nothing else."
    )
)

# Create the chain
chain = my_prompt_template_contract_info | openai_llm

# Function to get contract key information
def get_contract_keyinfo(contract_text):
    # Pass the input as a dictionary
    answer = chain.invoke(contract_text)  # Expecting a dictionary input
    return answer.content

# Function to convert JSON to DataFrame
def json_to_dataframe(json_string):
    try:
        data = json.loads(json_string)
        df = pd.DataFrame([data])  # Wrap in a list to ensure it's treated as a row
        return df
    except json.JSONDecodeError:
        print("Invalid JSON string provided.")
        return pd.DataFrame()

# Function to get contract information as a DataFrame
def get_contract_keyinfo_df(contract_text):
    json_data = get_contract_keyinfo(contract_text)
    return json_to_dataframe(json_data)

# # Example usage
# txt_content = "On January 15, 2023, ABC Corp entered into an agreement with XYZ Solutions to provide comprehensive IT consulting services."
# response = get_contract_keyinfo(txt_content)
# print("Raw JSON Response:")
# print(response)

# # Convert to DataFrame and print
# df_response = get_contract_keyinfo_df(txt_content)
# print("\nDataFrame Response:")
# print(df_response)
