import streamlit as st
import subprocess
import time
import os
from PIL import Image

st.set_page_config(page_title="Stock Market Analyzer", layout="wide")

st.title("Stock Market Analyzer")

# Input for stock symbols
symbols = st.text_input("Enter stock symbols (comma-separated)", "AAPL,GOOGL,MSFT,AMZN")

if st.button("Analyze"):
    # Run the Flask app in the background
    process = subprocess.Popen(["python", "app.py"])
    
    st.info("Analysis in progress... Please wait.")
    
    # Wait for the analysis to complete
    time.sleep(10)  # Adjust this based on how long your analysis typically takes
    
    # Display the results
    st.success("Analysis complete!")
    
    # Display the plots
    st.subheader("Analysis Results")
    
    plot_files = [f for f in os.listdir('static') if f.endswith('.png')]
    
    for plot_file in plot_files:
        image = Image.open(os.path.join('static', plot_file))
        st.image(image, caption=plot_file, use_column_width=True)
    
    # Clean up
    process.terminate()

st.sidebar.info("This app analyzes stock market data and provides insights.")
st.sidebar.warning("Disclaimer: This is not financial advice. Use at your own risk.")