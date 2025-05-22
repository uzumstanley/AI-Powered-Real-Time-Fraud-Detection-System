CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    account_id VARCHAR(255) NOT NULL,
    amount NUMERIC NOT NULL,
    location VARCHAR(255),
    event_time TIMESTAMP NOT NULL DEFAULT NOW(),
    is_fraud BOOLEAN,
    fraud_probability NUMERIC
);

CREATE TABLE alerts (
    alert_id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES transactions(transaction_id),
    alert_type VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);