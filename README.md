# Aave V2 Wallet Credit Score Generator

This repository contains a Python application that assigns credit scores (0–1000) to wallets based on their transaction history with the Aave V2 protocol on the Polygon network. The application processes a JSON file containing transaction data, engineers features, computes scores, and displays results using a Streamlit interface. An analysis of the scores is provided in `analysis.md`.

## Method Chosen

The credit scoring model uses a heuristic-based approach due to the absence of labeled data. The scoring logic rewards responsible behaviors (e.g., frequent deposits, timely repayments) and penalizes risky behaviors (e.g., high borrowing, liquidations). Key features include:

- **Transaction Counts**: Number of deposits, borrows, repays, redemptions, and liquidations.
- **USD Values**: Total transaction amounts in USD, adjusted for token decimals.
- **Borrow-to-Deposit Ratio**: Indicates leverage (high ratios lower the score).
- **Repayment Rate**: Proportion of borrows repaid (higher rates increase the score).
- **Asset Diversity**: Number of unique assets used (diversity increases the score).
- **Transaction Recency**: Days since the last transaction (recent activity increases the score).

A Random Forest Regressor is included as a placeholder for future supervised learning if labeled data becomes available. The heuristic scores are clipped to the range 0–1000.

## Architecture

The application follows a modular architecture:

1. **Data Ingestion**:
   - Input: JSON file with transaction data (e.g., `userWallet`, `action`, `actionData.amount`, `actionData.assetSymbol`).
   - Processing: Loaded into a Pandas DataFrame using `pd.json_normalize`.

2. **Feature Engineering**:
   - Features are computed per wallet, including transaction counts, USD values, ratios, and recency.
   - Token amounts are normalized (e.g., USDC: 6 decimals, WMATIC: 18 decimals) and converted to USD.

3. **Scoring**:
   - Heuristic scoring function assigns a base score of 500, adjusted by feature-based rewards and penalties.
   - Scores are normalized to 0–1000.

4. **Analysis**:
   - Generates `analysis.md` with score distribution (0–100, 100–200, ..., 900–1000) and behavioral insights for low (<200) and high (>=800) scoring wallets.
   - Saves a score distribution plot as `score_distribution.png`.

5. **User Interface**:
   - Streamlit app with file uploader, score table, analysis display, and visualization.

## Processing Flow

1. **Upload JSON File**:
   - User uploads a JSON file via the Streamlit interface.
   - File is saved temporarily as `temp.json`.

2. **Data Loading**:
   - JSON is parsed into a DataFrame, handling nested fields like `actionData`.

3. **Feature Engineering**:
   - Transactions are grouped by `userWallet`.
   - Features (e.g., transaction counts, USD values, ratios) are computed.

4. **Scoring**:
   - Heuristic function calculates scores based on features.
   - Results are stored in a DataFrame with `userWallet` and `credit_score`.

5. **Analysis**:
   - Scores are binned into ranges (0–100, 100–200, etc.).
   - Behavioral statistics (mean feature values) are computed for low (<200) and high (>=800) scoring wallets.
   - Distribution plot is saved, and analysis is written to `analysis.md`.

6. **Display**:
   - Streamlit displays the score table, analysis markdown, and distribution plot.
   - Temporary files are cleaned up.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/aave-credit-score.git
   cd aave-credit-score
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run credit_score_app.py
   ```

## Usage

1. Open the Streamlit app in your browser (typically at `http://localhost:8501`).
2. Upload a JSON file containing Aave V2 transaction data (see sample structure in the assignment).
3. View the generated credit scores, analysis, and score distribution plot.

## Files

- `credit_score_app.py`: Main application script.
- `analysis.md`: Analysis of wallet scores, including distribution and behavioral insights.
- `requirements.txt`: Python dependencies.
- `score_distribution.png`: Generated plot of score distribution (created after running the app).

## Notes

- The JSON file should match the structure provided (e.g., `userWallet`, `action`, `actionData`).
- The scoring model is heuristic-based; a supervised model can be implemented with labeled data.
- Update the `convert_to_usd` function if additional assets are present in the data.