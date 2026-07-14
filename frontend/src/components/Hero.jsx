import SearchBar from "./SearchBar";
import CategoryChips from "./CategoryChips";
import "../styles/hero.css";

export default function Hero({ onSearch, loading }) {
  return (
    <section className="hero">
      <h1>
        Find Your Next
        <span> Perfect Influencer</span>
      </h1>
      <p>
        Discover creators using AI semantic intelligence.
      </p>
      <SearchBar
        onSearch={onSearch}
        loading={loading}
      />
      <CategoryChips onSelect={onSearch} />
    </section>
  );
}
