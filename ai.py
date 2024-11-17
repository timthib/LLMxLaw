from llama_index.llms import OpenAI
from llama_index import ServiceContext, SimpleNodeParser, Prompt
from llama_index.core.indices.vector_store import GPTVectorStoreIndex
import pandas as pd
import json

# Set OpenAI API key
api_key = "your_openai_api_key"

# Initialize the OpenAI LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.3, api_key=api_key)

# Create the ServiceContext
service_context = ServiceContext.from_defaults(llm=llm)

# Define the prompt template
prompt = (
    "You are an AI assistant that extracts structured information from legal and contractual documents. "
    "Your task is to read the provided contract text and extract the following details:\n"
    "Contract Counterpart: The party or entity entering the contract.\n"
    "Signing Date: The date the contract was signed.\n"
    "Due Date: The deadline or due date for any obligations.\n"
    "Price: The monetary value or compensation stated in the contract.\n"
    "Prestation Summary: A brief summary of the services or goods described in the contract.\n"
    "If any piece of information is missing or unclear, return 'NA' for that field.\n\n"
    "Input Contract:\n"
    "{contract_text}\n\n"
    "Output JSON Format:\n"
    "{\n"
    '    "contract_counterpart": "Extracted Value or NA",\n'
    '    "signing_date": "Extracted Value or NA",\n'
    '    "due_date": "Extracted Value or NA",\n'
    '    "price": "Extracted Value or NA",\n'
    '    "prestation_summary": "Extracted Value or NA"\n'
    "}\n\n"
    "Make sure to output only the JSON, and nothing else."
)

custom_prompt = Prompt(template=extract_info_contract)

def get_contract_keyinfo(contract_content_txt):
    # Create a SimpleNode with the provided content
    parser = SimpleNodeParser()
    nodes = parser.create_nodes_from_documents([contract_content_txt])
    
    # Build an index for querying
    index = GPTVectorStoreIndex(nodes, service_context=service_context)
    
    # Query the index using the custom prompt
    query_engine = index.as_query_engine(service_context=service_context, text_qa_template=custom_prompt)
    answer = query_engine.query(contract_content_txt)
    
    return answer.response

def json_to_dataframe(json_string):
    try:
        data = json.loads(json_string)
        df = pd.DataFrame([data])  # Wrap in a list to ensure it's treated as a row
        return df
    except json.JSONDecodeError:
        print("Invalid JSON string provided.")
        return pd.DataFrame()

def get_contract_keyinfo_df(contract_content_txt):
    json_data = get_contract_keyinfo(contract_content_txt)
    return json_to_dataframe(json_data)



