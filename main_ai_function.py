import pdf
import langchain_ai
import esg_scoring
import pandas as pd

def ai_for_network(pdf_path):
    
    db_contract = pd.DataFrame()

    # Creating a DataFrame with potential companies that could have contracts with Koyeb
    sample_data = {
        "contract_counterpart": [
            "Amazon Web Services (AWS)",
            "Microsoft Azure",
            "Google Cloud Platform",
            "DigitalOcean",
            "IBM Cloud",
            "Linode",
            "Oracle Cloud Infrastructure"
        ],
        "signing_date": [
            "15/03/2024",
            "10/04/2024",
            "22/05/2024",
            "18/06/2024",
            "12/07/2024",
            "25/08/2024",
            "09/09/2024"
        ],
        "due_date": [
            "15/03/2025",
            "10/04/2025",
            "22/05/2025",
            "18/06/2025",
            "12/07/2025",
            "25/08/2025",
            "09/09/2025"
        ],
        "price": [
            "€1,500,000",
            "€2,000,000",
            "€1,800,000",
            "€1,200,000",
            "€1,750,000",
            "€1,100,000",
            "€2,250,000"
        ],
        "prestation_summary": [
            "Cloud hosting and compute resources",
            "Managed Kubernetes services",
            "Serverless function deployment",
            "Object storage and CDN integration",
            "AI and machine learning tools",
            "Edge computing services",
            "High-performance database solutions"
        ],
        "contract_valid": [
            "Yes",
            "Yes",
            "Yes",
            "No",
            "Yes",
            "No",
            "Yes"
        ]
    }

    db_contract = pd.DataFrame(sample_data)

    contract_content_txt = pdf.extract_text_from_pdf(pdf_path)
    contract_keyinfo = langchain_ai.get_contract_keyinfo_df(contract_content_txt)
    db_contract = pd.concat([db_contract, contract_keyinfo], ignore_index=True)
            


    db_esg_score = esg_scoring.comapany_esg_score(db_contract)

    db_esg_score['start_company'] = "Koyeb"
    db_esg_score['price'] = db_esg_score['price'].replace({'€': '', ',': ''}, regex=True).astype(float)
        
    
    db_summary = db_esg_score[["start_company","contract_counterpart","price"]]
        
    return db_summary

ai_for_network("data.pdf")