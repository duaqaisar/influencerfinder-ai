import { Search } from "lucide-react";
import { useState } from "react";
import "../styles/search.css";

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState("");

  const submit = () => {
    console.log("Searching for:", query);

    if (!query.trim()) return;

    onSearch(query);
  };
  return (
    <div className="search-wrapper">
      <div className="search-box">

        <Search size={22} className="search-icon" />

        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="Search creators, brands or topics..."
        />

        <button onClick={submit}>
          {loading ? "Searching..." : "Search"}
        </button>

      </div>
    </div>
  );
}
