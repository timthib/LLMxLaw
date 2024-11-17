import streamlit  as st
import pdf
import langchain_ai
import esg_scoring
import pandas as pd
import networkx as nx
from pyvis.network import Network
from fpdf import FPDF



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
# Displaying the DataFrame
st.write("Ongoing Contract Koyeb:")
st.write(db_contract)


st.title("Contract analyser")
pdf_path = st.file_uploader("Upload your  contract", type=["pdf"])

if st.button("Run Analysis"):
    if pdf_path is not None:
            contract_content_txt = pdf.extract_text_from_pdf(pdf_path)
            contract_keyinfo = langchain_ai.get_contract_keyinfo_df(contract_content_txt)
            db_contract = pd.concat([db_contract, contract_keyinfo], ignore_index=True)
            st.write(db_contract)

if st.button("Show NetworkX"):
    if pdf_path is not None:
            contract_content_txt = pdf.extract_text_from_pdf(pdf_path)
            contract_keyinfo = langchain_ai.get_contract_keyinfo_df(contract_content_txt)
            db_contract = pd.concat([db_contract, contract_keyinfo], ignore_index=True)
    db_esg_score = esg_scoring.comapany_esg_score(db_contract)
    db_esg_score['start_company'] = "Koyeb"
    db_esg_score['price'] = db_esg_score['price'].replace({'€': '', ',': ''}, regex=True).astype(float)

    # Create NetworkX graph
    G = nx.DiGraph()

    for _, row in db_esg_score.iterrows():
        # Add nodes
        G.add_node(row["start_company"], size=20, title="Koyeb")
        G.add_node(row["contract_counterpart"], size=row["price"] / 100000, title=row["contract_counterpart"])

        # Add edge
        G.add_edge(row["start_company"], row["contract_counterpart"])

    # Visualize using PyVis
    net = Network(notebook=False, height="600px", width="100%", bgcolor="#222222", font_color="white")

    # Add nodes and edges
    for node, data in G.nodes(data=True):
        net.add_node(node, size=data.get("size", 10), title=node)

    for start, end in G.edges():
        net.add_edge(start, end)

    # Save the network graph as HTML
    net.save_graph("network.html")

    # Read and display the HTML in Streamlit
    with open("network.html", "r") as f:
        html = f.read()

    st.components.v1.html(html, height=650)

# Add a dropdown to select a company
selected_company = st.selectbox(
    "Select a company from the list:",
    options=db_contract["contract_counterpart"].unique()
)

st.write(f"Selected Company: **{selected_company}**")

# Add a download button for a static PDF
pdf_content = """
NVIDIA: Contract Relationship and Risk Profile

Contract Details:

Supplier: Nvidia Inc.
Location: Shenzhen, Guangdong, China
Contracts: 1
Contract Duration: November 17, 2024 - unspecified end date or earlier termination
Products:
Model X1000: High-performance GPU
Model Y2000: Energy-efficient GPU
Quantity:
500 units of Model X1000
300 units of Model Y2000
Price:
EUR 5,000 per unit
Total contract value: EUR4,000,000 (exclusive of taxes)
Risks:

ESG Risk Rating: 12.2 (low risk)
Reputational Risks: No ongoing legal action or compliance issues. Potential concerns:
Intellectual property
Ethical sourcing
Geopolitical relations (supplier location in China)
Environmental Risks: No ongoing legal action or compliance issues. Issues:
High energy consumption in manufacturing
Electronic waste management
Social Risks: No ongoing legal action or compliance issues. Possible scrutiny:
Labor practices in manufacturing facilities in Shenzhen
"""

# Create and save the sample PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "Sample Contract", border=0, ln=1, align='C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.chapter_body(pdf_content)
pdf_output_path = "sample_contract.pdf"
pdf.output(pdf_output_path)

# Add a download button for the static PDF
with open(pdf_output_path, "rb") as f:
    st.download_button(
        label="Download Sample Contract PDF",
        data=f,
        file_name="Sample_Contract.pdf",
        mime="application/pdf"
    )