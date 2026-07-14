import "../styles/results.css";

export default function SearchResults({ loading, results }) {
  if (loading) {
    return (
      <div className="loading-card">
        Searching AI database...
      </div>
    );
  }

  if (!results.length) {
    return (
      <div className="loading-card">
        No influencers found for this search. Try a different topic.
      </div>
    );
  }

  return (
    <div className="results">
      {results.map((item) => (
        <div className="result-card" key={item.rank}>
          <div className="platform">
            {item.platform}
          </div>

          <h2>@{item.username}</h2>

          <p>
            {item.followers.toLocaleString()} Followers
          </p>

          <div className="score">
            AI Match
            <strong>
              {(item.overall_score * 100).toFixed(0)}%
            </strong>
          </div>

          <div className="confidence">
            Confidence {item.confidence_score}%
          </div>

          <small>
            {item.selection_reason}
          </small>
        </div>
      ))}
    </div>
  );
}
