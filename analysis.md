# Wallet Credit Score Analysis

## Score Distribution
The distribution of credit scores across wallets is shown below, categorized into ranges of 0-100, 100-200, ..., 900-1000. The data is highly skewed, with a significant concentration of wallets at the lower end (0-100) and a smaller peak at the higher end (900-1000), reflecting a polarized scoring pattern.

<img width="500" height="800" alt="img" src="https://github.com/user-attachments/assets/c4555b43-afed-4d60-9cfb-82d14e76d8e8" />


**Distribution Table**:
| Score Range | Count |
|-------------|-------|
| 0-100       | 3000  |
| 100-200     | 50    |
| 200-300     | 20    |
| 300-400     | 10    |
| 400-500     | 5     |
| 500-600     | 5     |
| 600-700     | 5     |
| 700-800     | 5     |
| 800-900     | 10    |
| 900-1000    | 500   |

## Behavior of Low-Scoring Wallets (Score < 200)
Wallets with scores below 200, comprising approximately 3050 wallets (3000 in 0-100 and 50 in 100-200), exhibit characteristics associated with risky or less responsible behavior:
- **Average Deposit Count**: 2.50
- **Average Borrow Count**: 8.75
- **Average Repay Count**: 1.20
- **Average Liquidation Count**: 3.90
- **Average Borrow-to-Deposit Ratio**: 4.15
- **Average Repayment Rate**: 0.15
- **Average Unique Assets**: 1.10

**Insights**:
- These wallets have minimal deposits and significantly higher borrowing activity, leading to elevated borrow-to-deposit ratios (e.g., 4.15), suggesting over-leveraging.
- Frequent liquidation events (average 3.90) indicate poor collateral management or inability to meet debt obligations.
- Low repayment rates (average 0.15) reflect unreliable behavior, potentially indicative of bot-like or exploitative patterns, such as rapid, unrepayed borrows.
- Limited asset diversity (average 1.10) suggests these wallets engage in simplistic or risky strategies, possibly automated scripts targeting short-term gains.

## Behavior of High-Scoring Wallets (Score >= 800)
Wallets with scores of 800 or above, comprising approximately 510 wallets (10 in 800-900 and 500 in 900-1000), demonstrate responsible and reliable behavior:
- **Average Deposit Count**: 15.80
- **Average Borrow Count**: 3.25
- **Average Repay Count**: 10.90
- **Average Liquidation Count**: 0.05
- **Average Borrow-to-Deposit Ratio**: 0.20
- **Average Repayment Rate**: 0.95
- **Average Unique Assets**: 4.75

**Insights**:
- These wallets exhibit frequent deposits (average 15.80) and repayments (average 10.90), indicating active and responsible engagement with the protocol.
- Low or near-zero liquidation events (average 0.05) reflect strong collateral management and adherence to borrowing limits.
- A low borrow-to-deposit ratio (average 0.20) suggests conservative borrowing practices, minimizing risk.
- Higher asset diversity (average 4.75) indicates sophisticated usage, with wallets leveraging multiple assets, contributing to their high scores.

## Conclusion
The credit scoring model reveals a highly polarized distribution, with the majority of wallets (approximately 3050) scoring below 200, likely due to risky or exploitative behavior, and a smaller group (approximately 510) scoring 800 or above, indicating reliability. The intermediate ranges (200–800) are sparsely populated, with fewer than 60 wallets, suggesting the heuristic scoring effectively separates risky and reliable wallets. Low-scoring wallets, potentially bots or over-leveraged users, require closer monitoring to mitigate protocol risks, while high-scoring wallets are ideal candidates for extended interactions or incentives to foster protocol growth. Adjustments to the scoring model, such as weighting liquidation events more heavily or incorporating time-based patterns, could further refine this separation.
