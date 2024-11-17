from character_network import CharacterNetworkGenerator
import gradio as gr
import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
load_dotenv()

def get_character_network(pdf_path):
    character_network_generator = CharacterNetworkGenerator()
    df=character_network_generator.build_dataframe_from_url()
    print(df)
    html = character_network_generator.draw_network_graph(df)
    urls = character_network_generator.generate_urls(df)

    return html,urls

def main():
    with gr.Blocks() as iface: 
        # Character Network Section
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Companies network</h1>")
                with gr.Row():
                    with gr.Column():
                        network_html = gr.HTML()
                        urls_textbox = gr.Textbox(label="Companies network", lines=10)
                    with gr.Column():
                        pdf_path = gr.Textbox(label="Contract path")
                        get_network_graph_button = gr.Button("Get the Relations Network")
                        get_network_graph_button.click(get_character_network, inputs=[pdf_path], outputs=[network_html, urls_textbox])

    iface.launch(share=True)

if __name__ == "__main__":
    main()