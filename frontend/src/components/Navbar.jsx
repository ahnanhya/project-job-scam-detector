import React from "react";

function Navbar({ onNavigate }) {
  return (
    <nav className="navbar">
      <div className="logo">
        <span className="logo-icon">🛡️</span>
        <span>JobGuard</span>
      </div>

      <button
        className="home-button"
        onClick={() => onNavigate("home")}
        aria-label="Return to home page"
      >
        <span aria-hidden="true">⌂</span>
        <span>Home</span>
      </button>
    </nav>
  );
}

export default Navbar;