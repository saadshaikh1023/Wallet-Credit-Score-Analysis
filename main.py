import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set page config for Streamlit
st.set_page_config(page_title="Aave V2 Wallet Credit Score", layout="wide")

# Function to load and preprocess JSON data
def load_data(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        df = pd.json_normalize(data)
        return df
    except Exception as e:
        st.error(f"Error loading JSON file: {e}")
        return None

# Function to convert amount to USD based on asset decimals
def convert_to_usd(row):
    amount = float(row['actionData.amount'])
    price_usd = float(row['actionData.assetPriceUSD'])
    # Adjust for token decimals (USDC: 6 decimals, WMATIC: 18 decimals)
    decimals = 6 if row['actionData.assetSymbol'] == 'USDC' else 18
    amount_normalized = amount / (10 ** decimals)
    return amount_normalized * price_usd

# Feature engineering
def engineer_features(df):
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    current_time = datetime.now()
    
    # Group by wallet
    wallet_features = df.groupby('userWallet').agg({
        'action': [
            'count',  # Total transactions
            lambda x: (x == 'deposit').sum(),  # Deposit count
            lambda x: (x == 'borrow').sum(),  # Borrow count
            lambda x: (x == 'repay').sum(),  # Repay count
            lambda x: (x == 'redeemunderlying').sum(),  # Redeem count
            lambda x: (x == 'liquidationcall').sum()  # Liquidation count
        ],
        'actionData.assetSymbol': 'nunique',  # Unique assets
        'timestamp': [
            lambda x: (current_time - x.max()).days  # Days since last transaction
        ]
    }).reset_index()
    
    # Rename columns
    wallet_features.columns = [
        'userWallet',
        'total_transactions',
        'deposit_count',
        'borrow_count',
        'repay_count',
        'redeem_count',
        'liquidation_count',
        'unique_assets',
        'days_since_last_tx'
    ]
    
    # Calculate USD values
    df['amount_usd'] = df.apply(convert_to_usd, axis=1)
    usd_values = df.groupby(['userWallet', 'action'])['amount_usd'].sum().unstack(fill_value=0).reset_index()
    usd_values.columns = [
        'userWallet',
        'deposit_usd',
        'borrow_usd',
        'repay_usd',
        'redeem_usd',
        'liquidation_usd'
    ]
    
    # Merge features
    wallet_features = wallet_features.merge(usd_values, on='userWallet', how='left').fillna(0)
    
    # Calculate borrow-to-deposit ratio
    wallet_features['borrow_to_deposit_ratio'] = (
        wallet_features['borrow_usd'] / (wallet_features['deposit_usd'] + 1e-6)
    )
    
    # Calculate repayment rate
    wallet_features['repayment_rate'] = (
        wallet_features['repay_count'] / (wallet_features['borrow_count'] + 1e-6)
    ).clip(upper=1.0)
    
    return wallet_features

# Compute heuristic credit score
def compute_heuristic_score(row):
    score = 500  # Base score
    # Reward deposits
    score += row['deposit_count'] * 20
    score += min(row['deposit_usd'] / 1000, 200)  # Cap USD contribution
    # Reward repayments
    score += row['repay_count'] * 30
    score += row['repayment_rate'] * 100
    # Penalize borrows and liquidations
    score -= row['borrow_count'] * 10
    score -= row['liquidation_count'] * 50
    score -= min(row['borrow_to_deposit_ratio'] * 50, 200)
    # Reward diversity and activity
    score += row['unique_assets'] * 10
    score -= row['days_since_last_tx'] * 0.5
    # Clip score to 0-1000
    return max(0, min(1000, score))

# Train ML model (if labeled data available, otherwise use heuristic)
def train_model(features):
    # Placeholder: In a real scenario, use labeled data to train
    # For now, return heuristic scores
    features['credit_score'] = features.apply(compute_heuristic_score, axis=1)
    return features[['userWallet', 'credit_score']]

# Streamlit app
def main():
    st.title("Aave V2 Wallet Credit Score Generator")
    st.write("Upload a JSON file containing Aave V2 transaction data to generate credit scores for each wallet.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp.json", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Load and process data
        df = load_data("temp.json")
        if df is not None:
            st.success("Data loaded successfully!")
            
            # Engineer features
            features = engineer_features(df)
            
            # Compute scores
            results = train_model(features)
            
            # Display results
            st.subheader("Wallet Credit Scores")
            st.dataframe(results)
            
            # Visualizations
            st.subheader("Score Distribution")
            fig, ax = plt.subplots()
            sns.histplot(results['credit_score'], bins=20, ax=ax)
            ax.set_xlabel("Credit Score")
            ax.set_ylabel("Count")
            st.pyplot(fig)
            
            # Clean up
            Path("temp.json").unlink(missing_ok=True)
        else:
            st.error("Failed to process the file. Please ensure it matches the expected format.")

if __name__ == "__main__":
    main()