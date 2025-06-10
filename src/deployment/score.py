import json
import os
import pandas as pd
import joblib
import glob, logging

def init():
    global model
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"),
        "packaging_quality_default_model",  # extra sub‑folder inside version dir
        "model.pkl"
    )
    model = joblib.load(model_path)

def run(raw_data):
    try:
        data = json.loads(raw_data)

        # Handle input format from Azure (with columns + data)
        df = pd.DataFrame(data['input_data']['data'], columns=data['input_data']['columns'])

        # Optional: Convert categorical columns to category dtype if needed
        categorical_cols = ['SupplierName', 'GarmentType', 'Material',
                            'ProposedFoldingMethod', 'ProposedLayout',
                            'Size', 'Collection']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype('category')

        # Make prediction
        preds = model.predict_proba(df)[:, 1]  # Assuming binary classification
        return preds.tolist()
    except Exception as e:
        return str(e)