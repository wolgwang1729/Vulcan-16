import React from 'react';

const Header = () => {
  return (
    <header className="bg-gray-900 border-b border-gray-700 shadow-lg">
      <div className="flex items-center justify-between px-6 py-4">
        {/* Logo and Project Name */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">V</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Vulcan-16</h1>
            <p className="text-gray-400 text-sm">Compiler & Virtual Machine</p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="hidden md:flex items-center space-x-8">
          <button className="text-gray-300 hover:text-white transition-colors duration-200 font-medium">
            Editor
          </button>
          <button className="text-gray-300 hover:text-white transition-colors duration-200 font-medium">
            Compiler
          </button>
          <button className="text-gray-300 hover:text-white transition-colors duration-200 font-medium">
            Monitor
          </button>
          <button className="text-gray-300 hover:text-white transition-colors duration-200 font-medium">
            Examples
          </button>
        </nav>
      </div>
    </header>
  );
};

export default Header;
