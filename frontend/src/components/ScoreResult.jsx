import React from "react";

const ScoreResult = ({ scoreResult }) => {
  if (!scoreResult) return null;

  return (
    <div className="score-result">
      <h2>Transaction Score</h2>
      <p>Score: {scoreResult.score}</p>
      <p>Is Fraudulent: {scoreResult.is_fraud ? "Yes" : "No"}</p>
    </div>
  );
};

export default ScoreResult;