import { useState } from "react";
import api from "../services/api";

export default function useSearch() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  const search = async (topic) => {
    if (!topic.trim()) return;

    setLoading(true);

    console.log("Searching:", topic);

    try {
      const response = await api.get("/influencers", {
        params: {
          topic: topic,
          top_n: 10,
        },
      });
    console.log(" API Response:", response.data);
    console.log("First item:", JSON.stringify(response.data[0], null, 2));
    const data = response.data;
    const list = Array.isArray(data) ? data : [];

    if (!Array.isArray(data)) {
        console.warn("API did not return an array:", data);
    }

    setResults(list);
    } catch (err) {
      console.error("❌ API Error:", err);

      if (err.response) {
        console.error("Status:", err.response.status);
        console.error("Data:", err.response.data);
      } else if (err.request) {
        console.error("No response received from backend.");
      } else {
        console.error("Error:", err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    results,
    search,
  };
}
