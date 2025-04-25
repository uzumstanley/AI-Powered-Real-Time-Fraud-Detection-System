**Bank Transaction Dataset for Fraud Detection**

Detailed Analysis of Transactional Behavior and Anomaly Detection

**About Dataset**

This dataset provides a detailed look into transactional behavior and financial activity patterns, ideal for exploring fraud detection and anomaly identification. It contains 2,512 samples of transaction data, covering various transaction attributes, customer demographics, and usage patterns. Each entry offers comprehensive insights into transaction behavior, enabling analysis for financial security and fraud detection applications.

**Key Features:**

TransactionID: Unique alphanumeric identifier for each transaction.
AccountID: Unique identifier for each account, with multiple transactions per account.
TransactionAmount: Monetary value of each transaction, ranging from small everyday expenses to larger purchases.
TransactionDate: Timestamp of each transaction, capturing date and time.
TransactionType: Categorical field indicating 'Credit' or 'Debit' transactions.
Location: Geographic location of the transaction, represented by U.S. city names.
DeviceID: Alphanumeric identifier for devices used to perform the transaction.
IP Address: IPv4 address associated with the transaction, with occasional changes for some accounts.
MerchantID: Unique identifier for merchants, showing preferred and outlier merchants for each account.
AccountBalance: Balance in the account post-transaction, with logical correlations based on transaction type and amount.
PreviousTransactionDate: Timestamp of the last transaction for the account, aiding in calculating transaction frequency.
Channel: Channel through which the transaction was performed (e.g., Online, ATM, Branch).
CustomerAge: Age of the account holder, with logical groupings based on occupation.
CustomerOccupation: Occupation of the account holder (e.g., Doctor, Engineer, Student, Retired), reflecting income patterns.
TransactionDuration: Duration of the transaction in seconds, varying by transaction type.
LoginAttempts: Number of login attempts before the transaction, with higher values indicating potential anomalies.
This dataset is ideal for data scientists, financial analysts, and researchers looking to analyze transactional patterns, detect fraud, and build predictive models for financial security applications. The dataset was designed for machine learning and pattern analysis tasks and is not intended as a primary data source for academic publications.
