import React, { useState } from "react";
import TransactionForm from "./components/TransactionForm";
import ScoreResult from "./components/ScoreResult";
import HistoryTable from "./components/HistoryTable";

const App = () => {
  const [scoreResult, setScoreResult] = useState(null);

  return (
    <div className="app">
      <h1>Fraud Detection System</h1>
      <TransactionForm setScoreResult={setScoreResult} />
      <ScoreResult scoreResult={scoreResult} />
      <HistoryTable />
    </div>
  );
};

export default App;