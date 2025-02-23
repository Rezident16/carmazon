import React, { useState, useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import { useHistory } from "react-router-dom";

import { useSearchBar } from "../../context/SearchBarClass";

function SearchBar({ items }) {
  const [searchTerm, setSearchTerm] = useState("");

  const user = useSelector((state) => state.session.user);

  const { searchClass } = useSearchBar();

  const history = useHistory();

  const searchBarClassName = searchTerm ? "search_terms" : "empty_search_bar";
  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleClickOutside = (event) => {
      if (!event.target.classList.contains("search_term_target")) {
        setSearchTerm("");
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const filteredItems = items.filter(
    (item) =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.brand.toLowerCase().includes(searchTerm.toLowerCase())
  );
  

  return (
    <div className={searchClass}>
        <div className="search_bar_glass">
        <i class="fa-solid fa-magnifying-glass"></i>
      <input
        type="text"
        placeholder="Search by name or brand..."
        value={searchTerm}
        onChange={handleInputChange}
        className="search_bar search_term_target"
      />
        </div>
      <div className={searchBarClassName}>
        {searchTerm && filteredItems.length > 0 ? (
          filteredItems
            .map((item) => (
              <div
                onClick={() => {
                  history.push(`/items/${item.id}`);
                  setSearchTerm("");
                }}
                className="search_term_result search_term_target"
                key={item.id}
              >
                <img
                  className="search_term_img search_term_target"
                  src={item.preview_img}
                  alt={item.name}
                />
                <div className="item_name_brand_search search_term_target">
                  <h4 className="search_term_target">{item.name}</h4>
                  <p className="search_term_target">{item.brand}</p>
                </div>
              </div>
            ))
            .slice(0, 5)):
            (<div
              className="search_term_result search_term_target"
              style={{cursor: "default"}}
            >
              <div className="item_name_brand_search search_term_target"
              
              >
                <p className="search_term_target"
                style={{fontFamily: "Poppins"}}
                >Nothing here yet. Try searching for something else.</p>
              </div>
            </div>)
            }
      </div>
    </div>
  );
}

export default SearchBar;
