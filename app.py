import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pycaret.classification import load_model, predict_model

st.title("Interactive PyCaret Model Deployment")

# Upload a PyCaret model file
uploaded_model = st.file_uploader("best_classification_model", type=["pkl"])

if uploaded_model:
    # Save and load the uploaded model
    with open("best_classification_model.pkl", "wb") as f:
        f.write(uploaded_model.getbuffer())

    model = load_model("best_classification_model")  # Load PyCaret model
    st.success("Model uploaded and loaded successfully!")

    # Dynamically ask for feature inputs
    st.subheader("Enter Feature Values")

    # Extract feature names from the PyCaret model
    feature_names = list(model.feature_names_in_)  # Expected features
    user_inputs = {}

    for feature in feature_names:
        user_inputs[feature] = st.text_input(f"Enter {feature}")

    # Convert input to DataFrame
    if st.button("Predict"):
        try:
            # Convert input values to the correct types
            input_df = pd.DataFrame([user_inputs]).apply(pd.to_numeric, errors='coerce')

            # Check for missing values
            if input_df.isnull().values.any():
                st.error("Please enter valid numerical values for all features.")
            else:
                # Predict using PyCaret
                predictions = predict_model(model, data=input_df)
                st.success(f"Prediction: {predictions['prediction_label'][0]}")
        except Exception as e:
            st.error(f"Error: {e}")
