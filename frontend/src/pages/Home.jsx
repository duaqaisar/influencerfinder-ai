import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import SearchResults from "../components/SearchResults";
import useSearch from "../hooks/useSearch";

import detective from "../assets/detective.png";

import "../styles/home.css";

export default function Home() {

  const {
    loading,
    results,
    search
  } = useSearch();

  return (

    <div className="home">

      <Navbar />

      <Hero
        onSearch={search}
        loading={loading}
      />

      <SearchResults
        loading={loading}
        results={results}
      />

      <img
        src={detective}
        className="home-detective"
        alt="AI Detective"
      />

    </div>

  );
}
