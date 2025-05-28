import React, { useEffect, useState } from "react";
import axios from "axios";

const HistoryTable = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    // Fetch transaction history from the backend
    const fetchTransactions = async () => {
      try {
        const response = await axios.get("http://localhost:8000/transactions/history");
        setTransactions(response.data);
      } catch (error) {
        console.error("Error fetching transaction history:", error);
      }
    };

    fetchTransactions();
  }, []);

  return (
    <div className="history-table">
      <h2>Transaction History</h2>
      {transactions.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Transaction ID</th>
              <th>Account ID</th>
              <th>Score</th>
              <th>Is Fraud</th>
              <th>Event Time</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.transaction_id}>
                <td>{transaction.transaction_id}</td>
                <td>{transaction.account_id}</td>
                <td>{transaction.score.toFixed(2)}</td>
                <td>{transaction.is_fraud ? "Yes" : "No"}</td>
                <td>{new Date(transaction.event_time).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No transactions found.</p>
      )}
    </div>
  );
};

export default HistoryTable;