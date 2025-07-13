import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sys
import numpy as np


df = pd.DataFrame([["Supplier A", "Method 3", "Layout D", 45],["Supplier A", "Method 3", "Layout D",45],['Supplier B','Method 1','Layout D',45]] , columns=["Supplier", "Best Folding Method", "Best Layout", "Suggested Units per Package"])
# --- Page Configuration and Model Loading ---

# Set a title for the browser tab
st.set_page_config(page_title="Smart Hub", layout="wide")


# --- UI Tabs ---

dashboard, suggest, risk, cost = st.tabs(["Smart Hub", "Suggest Package", "Risk", "Estimate Cost"])

with dashboard:
    st.title("📈 Smart Hub Dashboard")
    looker_studio_url = "https://lookerstudio.google.com/embed/reporting/f784b594-c7be-4ff7-8b2d-1a9ac40b7ba6/page/p_7na3c7dntd"
    
    # Add some introductory text
    st.markdown("### Welcome to the Smart Hub")
    st.info("This dashboard provides a real-time overview of key metrics. Use the tabs above to explore other features.")
    
    components.iframe(looker_studio_url, height=1200, scrolling=True)

with suggest:
    st.title("📦 Suggest Packaging")
    st.write("Select the product and package configuration to get a recommendation.")

    # List of available suppliers
    garment_options = ['Pants', 'Blouse', 'Skirt', 'Jacket', 'Suit', 'Hoodie', 'Coat',
       'Shorts', 'Shirt', 'T-Shirt', 'Dress', 'Sweater']
    material_options = ['Polyester', 'Linen', 'Silk', 'Denim', 'Cotton', 'Wool']
    size_options = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
    collection_options = ['Summer', 'Winter']
    proposed_folding_method = ['Method2', 'Method1', 'Method3']


    
    # Use a form to group inputs and the submit button
    with st.form(key="suggestion_form"):
        st.write("Select your product configuration")
        # The key 'selected_supplier' will hold the string of the chosen supplier
        garment_selected = st.selectbox("Garment Type", garment_options, key='garment', placeholder='Select Garment Type', index=None)
        material_selected = st.selectbox("Material", material_options, key="material", index=None, placeholder="Select Material")
        weight_selected = st.number_input("Weight (kg)", min_value=0.0, max_value=5.0, value=1.0, step=0.01, key='weight')
        size_selected = st.selectbox("Size", size_options, key="size", index=None, placeholder="Select Product Size")
        collection_selected = st.selectbox("Collection", collection_options, key="collection", index=None, placeholder="Select Collection")



        # The "Suggest" button for the form
        submitted = st.form_submit_button("Suggest Package", type="primary")

        if submitted:
            st.table(data=df)



with risk:
    st.title("⚠️ Risk Analysis")
    st.info("This section is under construction. Risk analysis features will be available soon.")
    # You can add placeholder components here


with cost:
    st.title("💰 Estimate Cost")
    st.info("This section is under construction. Cost estimation tools will be available soon.")
    # You can add placeholder components here

