import React, { useState } from 'react';

const JackEditor = () => {
  const [code, setCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState('assembly');
  const [output, setOutput] = useState('');
  const [status, setStatus] = useState('');

  const handleCodeChange = (event) => {
    setCode(event.target.value);
  };

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  const handleSend = async () => {
    if (!code.trim()) {
      setStatus('Please enter some code before compiling');
      setOutput('// No code to compile');
      return;
    }

    setIsLoading(true);
    setOutput('Compiling...');
    
    try {
      const blob = new Blob([code], { type: 'text/plain' });
      
      const getFileExtension = (lang) => {
        switch (lang) {
          case 'assembly': return 'asm';
          case 'jack': return 'jack';
          case 'c': return 'c';
          case 'cpp': return 'cpp';
          case 'python': return 'py';
          case 'javascript': return 'js';
          default: return 'txt';
        }
      };
      
      const fileExtension = getFileExtension(language);
      const file = new File([blob], `code.${fileExtension}`, { type: 'text/plain' });
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('language', language);

      const testresponse = await fetch(`${import.meta.env.VITE_BACKEND_URL}/test`, {
        method: 'GET',
      });
      const testresult = await testresponse.json();
      console.log('Test response:', testresult);
      
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/asmtohack`, {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      console.log('Backend response:', result);
      
      if (result.success) {
        setOutput(result.hack_code);
      } else {
        setOutput(`Error: ${result.message || result.error}`);
      }
      
    } catch (error) {
      console.error('Error sending file:', error);
      setOutput('Error: Unable to connect to backend server');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setCode('');
    setOutput('');
    setStatus('Editor cleared');
  };

  const handleRun = () => {
    console.log('Running code:', code);
    setOutput('// Run functionality not yet implemented');
  };

  const getPlaceholderText = (lang) => {
    switch (lang) {
      case 'assembly': return '// Write your Assembly code here...';
      case 'jack': return '// Write your Jack code here...';
      case 'vm': return '// Write your VM code here...';
      default: return '// Write your code here...';
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-gray-800 px-4 py-2 border-b border-gray-700">
        <h2 className="text-lg font-semibold text-gray-100">Multi-Language Code Editor</h2>
      </div>

      {/* Action Buttons */}
      <div className="bg-gray-800 px-4 py-3 border-t border-gray-700 flex gap-3">
        <select
          value={language}
          onChange={handleLanguageChange}
          className="bg-gray-700 text-white px-3 py-2 rounded-md border border-gray-600 
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="assembly">Assembly</option>
          <option value="jack">Jack</option>
          <option value="vm">VM</option>
        </select>

        <button
          onClick={handleSend}
          disabled={isLoading}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 
                     text-white px-6 py-2 rounded-md font-medium transition-colors
                     disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
          </svg>
          <span>{isLoading ? 'Processing...' : 'Compile'}</span>
        </button>
        
        <button
          onClick={handleRun}
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 
                     rounded-md font-medium transition-colors flex items-center space-x-2"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
          </svg>
          <span>Run</span>
        </button>
        
        <button
          onClick={handleClear}
          className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 
                     rounded-md font-medium transition-colors"
        >
          Clear
        </button>
        
        <div className="flex-1"></div>
        
        <span className="text-gray-400 text-sm self-center">
          Lines: {code.split('\n').length} | Characters: {code.length}
        </span>
      </div>

      {/* Status Bar */}
      {status && (
        <div className="bg-gray-750 px-4 py-2 border-b border-gray-700">
          <span className="text-sm text-gray-300">{status}</span>
        </div>
      )}

      {/* Split Editor and Output Area */}
      <div className="flex-1 p-4 flex gap-4">
        {/* Code Editor */}
        <textarea
          value={code}
          onChange={handleCodeChange}
          placeholder={getPlaceholderText(language)}
          className="w-1/2 h-full bg-gray-800 text-gray-100 p-4 border border-gray-600 
                     rounded-lg font-mono text-sm resize-none focus:outline-none 
                     focus:ring-2 focus:ring-blue-500 focus:border-transparent
                     placeholder-gray-400"
          style={{ minHeight: '400px' }}
        />

        {/* Output Display */}
        <pre
          className="w-1/2 h-full bg-gray-800 text-green-400 p-4 border border-gray-600 
                     rounded-lg font-mono text-sm overflow-auto"
          style={{ minHeight: '400px' }}
        >
          {output || '// Output will be displayed here...'}
        </pre>
      </div>
    </div>
  );
};

export default JackEditor;
