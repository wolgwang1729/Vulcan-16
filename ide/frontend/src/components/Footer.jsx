import React from 'react';
import VLogo from '../assets/PixelatedV.png';

const Footer = () => {
  return (
    <footer className="bg-gray-900 border-t border-gray-700 mt-auto">
      {/* Main Footer Content */}
      <div className="px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {/* Project Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-3">
              <img src={VLogo} alt="Vulcan Logo" className="w-10 h-10 rounded-lg" />
              <h3 className="text-lg font-semibold text-white">Vulcan-16</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed mb-3">
              A complete 16-bit computer system with compiler, virtual machine, and assembler. 
              Built from the ground up for educational and development purposes.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-semibold text-white mb-3">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                  API Reference
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                  Examples
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                  Tutorials
                </a>
              </li>
            </ul>
          </div>

          {/* Tools & Resources */}
          <div>
            <h4 className="text-sm font-semibold text-white mb-3">Tools</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                  Code Editor
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                  Assembler
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                  VM Translator
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                  Jack Compiler
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="bg-gray-800 px-6 py-4 border-t border-gray-700">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-3 md:space-y-0">
          {/* Copyright */}
          <div className="text-sm text-gray-400">
            © 2024 Vulcan-16 Project. Built with ❤️ for learning and development.
          </div>

          {/* Social/External Links */}
          <div className="flex items-center space-x-4">
            <a href="https://github.com/wolgwang1729" className="text-gray-400 hover:text-white transition-colors duration-200">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
            <div className="flex items-center space-x-2 text-sm text-gray-400">
              <span>Made with React & Tailwind CSS</span>
            </div>
          </div>
        </div>
      </div>

    </footer>
  );
};

export default Footer;
