import pandas as pd
import networkx as nx
from pyvis.network import Network

class CharacterNetworkGenerator():
    def __init__(self):
        pass

    def draw_network_graph(self, relationship_df):
        relationship_df = relationship_df.sort_values('price', ascending=False).head(200)

        G = nx.from_pandas_edgelist(
            relationship_df, 
            source='Company 1', 
            target='Company 2', 
            edge_attr='price',
            create_using=nx.Graph()
        )

        net = Network(notebook=True, width="1000px", height="700px", bgcolor="#222222", font_color="white", cdn_resources="remote")

        # Set node sizes and colors
        for node in G.nodes():
            if node in relationship_df['Company 1'].values:
                total_price = relationship_df[relationship_df['Company 1'] == node]['price'].sum()
                G.nodes[node]['size'] = 60 # Increase variability by adjusting divisor
                G.nodes[node]['color'] = 'white'
            else:
                total_price = relationship_df[relationship_df['Company 2'] == node]['price'].sum()
                G.nodes[node]['size'] = 10 + (total_price / 100000)  # Increase variability by adjusting divisor
                score = relationship_df.loc[relationship_df['Company 2'] == node, 'score'].values[0]
                red = int((score / 100) * 255)
                green = int((1 - score / 100) * 255)
                G.nodes[node]['color'] = f'rgb({red},{green},0)'

        # Set edge widths based on 'price'
        for u, v, d in G.edges(data=True):
            d['width'] = d['price'] / 1000000  # Adjust the divisor as needed for scaling

        net.from_nx(G)
        html = net.generate_html()
        html = html.replace("'", "\"")

        output_html = f"""<iframe style="width: 100%; height: 600px;margin:0 auto" name="result" allow="midi; geolocation; microphone; camera;
        display-capture; encrypted-media;" sandbox="allow-modals allow-forms
        allow-scripts allow-same-origin allow-popups
        allow-top-navigation-by-user-activation allow-downloads" allowfullscreen=""
        allowpaymentrequest="" frameborder="0" srcdoc='{html}'></iframe>"""
        
        return output_html

    data = {
        'Company 1': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',],
        'Company 2': ['K', 'L', 'M', 'N', 'O', 'P', 'R', 'S'],
        'price': [1000000, 2000000, 1500000, 3000000, 2500000, 3500000,4500000, 5000000],
        'score': [10, 20, 30, 40, 50, 60, 70, 80]
    }

    relationship_df = pd.DataFrame(data)

    # Call the function with the synthetic dataframe
    output_html = draw_network_graph(None, relationship_df)

    # Save the output HTML to a file
    output_file_path = 'network_graph.html'
    with open(output_file_path, 'w') as file:
        file.write(output_html)

    print(f"Network graph saved to {output_file_path}")


    def generate_urls(self, relationship_df):
            urls = ["https://drive.google.com/file/d/1DXSwGLBvj9Uk1I4sHwICxAxTCyLOhy4E/view?usp=sharing" for _ in range(len(relationship_df))]
            return "\n".join(urls)

    def build_dataframe_from_url(url):
        
        # Extracting the required information
        company1 = ['Koyeb', 'Koyeb', 'Koyeb']
        company2 = ['IBM', 'NVIDIA', 'Amazon']
        price = [1000000, 2000000, 1500000]
        score = [80, 20, 50]
    
        # Building the dictionary
        data_dict = {
            'Company 1': company1,
            'Company 2': company2,
            'price': price,
            'score': score
        }
        
        # Converting to DataFrame
        df = pd.DataFrame(data_dict)
        return df

