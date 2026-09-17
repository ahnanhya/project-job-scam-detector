import React from "react";

function Navbar({ currentPage, onNavigate, theme, onToggleTheme }) {
  return (
    <nav className="navbar">
      <div className="logo">
        <span className="logo-icon">🛡️</span>
        <span>JobGuard</span>
      </div>

      <div className="nav-links">
        <button
          className={currentPage === "home" ? "nav-button home-nav-button active" : "nav-button home-nav-button"}
          onClick={() => onNavigate("home")}
        >
          Home
        </button>

        <button
          className={currentPage === "dashboard" ? "nav-button active" : "nav-button"}
          onClick={() => onNavigate("dashboard")}
        >
          Dashboard
        </button>

        <button
          className="theme-toggle"
          onClick={onToggleTheme}
          aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
          title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
        >
          <span className="theme-toggle-icon" aria-hidden="true">
            {theme === "dark" ? "☀" : "☾"}
          </span>
          <span>{theme === "dark" ? "Light" : "Dark"}</span>
        </button>
      </div>
    </nav>
  );
}

export default Navbar;