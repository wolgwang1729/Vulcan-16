import React from 'react';
import VLogo from '../assets/PixelatedV.png';
import { NavLink } from "react-router-dom";

const Header = () => {
  return (
    <header className="bg-gray-900 border-b border-gray-700 shadow-lg">
      <div className="flex items-center justify-between px-6 py-4">
        {/* Logo and Project Name */}
        <div className="flex items-center space-x-3">
          <img src={VLogo} alt="Vulcan Logo" className="w-10 h-10 rounded-lg" />
          <div>
            <h1 className="text-2xl font-bold text-white">Vulcan-16</h1>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="hidden md:flex items-center space-x-8">
          <a
            href="https://github.com/wolgwang1729/Vulcan-16"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-300 hover:text-white transition-colors duration-200 font-medium"
          >
            GitHub
          </a>
          <NavLink
            to="/"
            className="text-gray-300 hover:text-white transition-colors duration-200 font-medium"
          >
            Compiler
          </NavLink>
          <NavLink
            to="/hardware-simulator"
            className="text-gray-300 hover:text-white transition-colors duration-200 font-medium"
          >
            Hardware Simulator
          </NavLink>
          {/* <button className="text-gray-300 hover:text-white transition-colors duration-200 font-medium">
            Monitor
          </button>
          <button className="text-gray-300 hover:text-white transition-colors duration-200 font-medium">
            Examples
          </button> */}
        </nav>
      </div>
    </header>
  );
};

export default Header;
