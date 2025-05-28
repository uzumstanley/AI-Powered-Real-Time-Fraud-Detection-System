import React, { useEffect, useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [transactions, setTransactions] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await axios.get("http://localhost:8000/transactions/history");
        setTransactions(response.data);
      } catch (err) {
        setTransactions([]);
      }
    };

    const fetchAlerts = async () => {
      // You can replace this with a real API call if you implement alerts in backend
      setAlerts(
        transactions
          .filter((tx) => tx.is_fraud === true)
          .map((tx, idx) => ({
            id: `alert_${idx}`,
            transaction_id: tx.id || tx.transaction_id || idx,
            type: "HIGH_RISK",
            time: tx.event_time,
          }))
      );
    };

    fetchTransactions();
    // fetchAlerts will run after transactions are loaded
  }, []);

  useEffect(() => {
    // Update alerts when transactions change
    setAlerts(
      transactions
        .filter((tx) => tx.is_fraud === true)
        .map((tx, idx) => ({
          id: `alert_${idx}`,
          transaction_id: tx.id || tx.transaction_id || idx,
          type: "HIGH_RISK",
          time: tx.event_time,
        }))
    );
  }, [transactions]);

  return (
    <div className="dashboard">
      <h1>Fraud Detection Dashboard</h1>
      <h2>Recent Transactions</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Account ID</th>
            <th>Amount</th>
            <th>Location</th>
            <th>Time</th>
            <th>Fraud?</th>
            <th>Anomaly Score</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx) => (
            <tr key={tx.id || tx.transaction_id}>
              <td>{tx.id || tx.transaction_id}</td>
              <td>{tx.account_id}</td>
              <td>{tx.amount}</td>
              <td>{tx.location}</td>
              <td>{new Date(tx.event_time).toLocaleString()}</td>
              <td>{tx.is_fraud ? "Yes" : "No"}</td>
              <td>{tx.fraud_probability !== undefined ? tx.fraud_probability.toFixed(4) : ""}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Alerts</h2>
      <ul>
        {alerts.map((alert) => (
          <li key={alert.id}>
            Alert: {alert.type} for Transaction {alert.transaction_id} at {new Date(alert.time).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;