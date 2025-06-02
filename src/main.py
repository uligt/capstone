import argparse
import lightgbm as lgb
import mlflow
import mlflow.sklearn
import numpy as np
import os
import pandas as pd
import polars as pl
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

def main():
    """Main function of the script."""

    # input and output arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="path to input data")
    parser.add_argument("--test_train_ratio", type=float, required=False, default=0.25)
    parser.add_argument("--n_estimators", required=False, default=100, type=int)
    parser.add_argument("--learning_rate", required=False, default=0.1, type=float)
    parser.add_argument("--registered_model_name", type=str, help="model name")
    args = parser.parse_args()
   
    # Start Logging
    mlflow.start_run()

    # enable autologging
    mlflow.sklearn.autolog()

    ###################
    #<prepare the data>
    ###################
    print(" ".join(f"{k}={v}" for k, v in vars(args).items()))
    print("input data:", args.data)

    df = pl.read_excel(source="./data/full_join.xlsx", sheet_name="Sheet1")
    df = df.with_columns([
        pl.col("CostImpact (€)").cast(pl.Float64, strict=False),
    ])

    mlflow.log_metric("num_samples", df.shape[0])
    mlflow.log_metric("num_features",df.shape[1] - 1)

    df_input = (
        df
        .filter(pl.col("PackagingQuality").is_in(["Bad", "Good"])) 
        .sort("DateOfReport")                                      
        .select([                                                 
            "SupplierName",
            "GarmentType",
            "Material",
            "Weight",
            "ProposedUnitsPerCarton",
            "ProposedFoldingMethod",
            "ProposedLayout",
            "Size",
            "Collection",
            "PackagingQuality"
        ])
    )
    # Convert Polars to Pandas
    df_pd = df_input.to_pandas()

    # Encode target variable
    df_pd["PackagingQuality"] = df_pd["PackagingQuality"].map({"Good": 1, "Bad": 0})

    # Define features and target
    X = df_pd.drop(columns=["PackagingQuality"])
    y = df_pd["PackagingQuality"]
    categorical_features = X.select_dtypes(include="object").columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    ####################
    #</prepare the data>
    ####################

    ##################
    #<train the model>
    ##################
    #weights
    class_weights = np.where(y_train == 1, 1, 4)  

    # Instantiate the LightGBM classifier
    model_lgb = lgb.LGBMClassifier(
        objective='binary',
        metric='auc',
        boosting_type='gbdt',
        n_estimators=1000,
        learning_rate=0.05,
        random_state=42
    )

    for c in categorical_features:
        X_train[c] = X_train[c].astype("category")
        X_test[c] = X_test[c].astype("category")

    actual_categorical_in_train = [col for col in categorical_features if col in X_train.columns and X_train[col].dtype.name == 'category']

    # Train the model
    model_lgb.fit(X_train, y_train, sample_weight=class_weights,categorical_feature=actual_categorical_in_train)

    # Make predictions on the test set
    y_pred_lgb = model_lgb.predict(X_test)
    y_proba_lgb = model_lgb.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, y_pred_lgb))
    ###################
    #</train the model>
    ###################

    ##########################
    #<save and register model>
    ##########################
    # Registering the model to the workspace
    print("Registering the model via MLFlow")
    mlflow.sklearn.log_model(
        sk_model=model_lgb,
        registered_model_name="packaging_quality_default_model",
        artifact_path="packaging_quality_default_model",
    )

    # Saving the model to a file
    mlflow.sklearn.save_model(
        sk_model=model_lgb,
        path=os.path.join("packaging_quality_default_model", "trained_model"),
    )
    ###########################
    #</save and register model>
    ###########################
    
    # Stop Logging
    mlflow.end_run()

if __name__ == "__main__":
    main()
