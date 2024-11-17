import pandas as pd

esg_score = {
    "company_name": [
        "Amazon Web Services (AWS)",
        "Microsoft Azure",
        "Google Cloud Platform",
        "DigitalOcean",
        "IBM Cloud",
        "Linode",
        "Oracle Cloud Infrastructure",
        "Nvidia Inc."
    ],
    "esg_score": [65, 75, 80, 70, 78, 68, 72, 85]
}

# Create the DataFrame
esg_df = pd.DataFrame(esg_score)

def comapany_esg_score(companies_list, esg_scoring=esg_df):
    merged = pd.merge(companies_list, esg_df, how='left', left_on='contract_counterpart', right_on='company_name')
    return merged
