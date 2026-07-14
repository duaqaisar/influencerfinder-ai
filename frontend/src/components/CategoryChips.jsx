import { useState } from "react";
import "../styles/chips.css";

const categories = [
  "AI",
  "Gaming",
  "Fashion",
  "Health",
  "Finance",
  "Tech"
];

export default function CategoryChips({ onSelect }) {
  const [active, setActive] = useState(null);

  const handleClick = (item) => {
    setActive(item);
    if (onSelect) onSelect(item);
  };

  return (
    <div className="chips">
      {categories.map((item) => (
        <button
          key={item}
          className={`chip ${active === item ? "active" : ""}`}
          onClick={() => handleClick(item)}
        >
          {item}
        </button>
      ))}
    </div>
  );
}
