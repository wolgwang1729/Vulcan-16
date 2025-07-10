import React, { useState, useEffect } from 'react';
import { 
  FaFolder, 
  FaFolderOpen, 
  FaFile, 
  FaPlus, 
  FaTimes, 
  FaCheck,
  FaPlay,
  FaSpinner,
  FaChevronRight,
  FaChevronDown
} from 'react-icons/fa';
import { AiOutlineFile } from 'react-icons/ai';

const JackEditor = () => {
  // File system state
  const [fileSystem, setFileSystem] = useState([
    {
      id: 'folder-1',
      name: 'Jack Sample Code1',
      type: 'folder',
      children: [
        { id: 'file-1', name: 'main.jack', type: 'file', content: '// Jack code here' },
        { id: 'file-2', name: 'math.vm', type: 'file', content: '// VM code here' },
      ],
    },
  ]);

  const [openFiles, setOpenFiles] = useState([]);
  const [activeFileId, setActiveFileId] = useState(null);
  const [output, setOutput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [newItemName, setNewItemName] = useState('');
  const [creatingItem, setCreatingItem] = useState(null); 
  const [currentFolder, setCurrentFolder] = useState(null);
  const [newItemParentId, setNewItemParentId] = useState(null);

  const findFile = (id, items = fileSystem) => {
    for (const item of items) {
      if (item.id === id) return item;
      if (item.children) {
        const found = findFile(id, item.children);
        if (found) return found;
      }
    }
    return null;
  };

  const activeFile = findFile(activeFileId);

  const handleFileSelect = (fileId) => {
    const file = findFile(fileId);
    if (!file) return;

    setActiveFileId(fileId);
    
    // Add to open files if not already open
    if (!openFiles.some(f => f.id === fileId)) {
      setOpenFiles([...openFiles, file]);
    }
  };

  // Handle file content change
  const handleFileContentChange = (content) => {
    if (!activeFileId) return;

    const updateContent = (items) => 
      items.map(item => {
        if (item.id === activeFileId) {
          return { ...item, content };
        }
        if (item.children) {
          return { ...item, children: updateContent(item.children) };
        }
        return item;
      });

    setFileSystem(updateContent(fileSystem));
    
    // Update open files
    setOpenFiles(openFiles.map(file => 
      file.id === activeFileId ? { ...file, content } : file
    ));
  };

  // Close a file
  const handleCloseFile = (fileId, e) => {
    e.stopPropagation();
    const newOpenFiles = openFiles.filter(file => file.id !== fileId);
    setOpenFiles(newOpenFiles);
    
    if (activeFileId === fileId) {
      setActiveFileId(newOpenFiles.length > 0 ? newOpenFiles[0].id : null);
    }
  };

  // Create new item
  const handleCreateItem = (type, parentId = null) => {
    setCreatingItem(type);
    setNewItemParentId(parentId);
    setNewItemName('');
  };

  // Save new item
  const handleSaveNewItem = () => {
    if (!newItemName.trim()) {
      setCreatingItem(null);
      setNewItemParentId(null);
      return;
    }

    const newItem = {
      id: `${creatingItem}-${Date.now()}`,
      name: newItemName,
      type: creatingItem,
      ...(creatingItem === 'file' 
        ? { content: '', extension: newItemName.split('.').pop() }
        : { children: [] })
    };

    const addItem = (items) => {
      if (newItemParentId === null) return [...items, newItem];
      
      return items.map(item => {
        if (item.id === newItemParentId) {
          return { ...item, children: [...(item.children || []), newItem] };
        }
        if (item.children) {
          return { ...item, children: addItem(item.children) };
        }
        return item;
      });
    };

    setFileSystem(addItem(fileSystem));
    setCreatingItem(null);
    setNewItemParentId(null);
    
    if (creatingItem === 'file') {
      handleFileSelect(newItem.id);
    }
  };

  const handleCompile = async () => {
    if (!activeFile || isLoading) return;
    
    setIsLoading(true);
    setOutput('Compiling...');
    
    try {
      const extension = activeFile.name.split('.').pop();
      let language;
      
      switch(extension) {
        case 'asm': language = 'assembly'; break;
        case 'jack': language = 'jack'; break;
        case 'vm': language = 'vm'; break;
        default: 
          setOutput(`Error: Unsupported file type (.${extension})`);
          setIsLoading(false);
          return;
      }
      
      const blob = new Blob([activeFile.content], { type: 'text/plain' });
      const file = new File([blob], activeFile.name, { type: 'text/plain' });
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('language', language);

      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/asmtohack`, {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      
      if (result.success) {
        setOutput(result.hack_code || 'Compilation successful');
      } else {
        setOutput(`Error: ${result.message || result.error}`);
      }
    } catch (error) {
      console.error('Error compiling:', error);
      setOutput('Error: Unable to connect to backend server');
    } finally {
      setIsLoading(false);
    }
  };

  const renderFileTree = (items, depth = 0) => (
    <ul className={`pl-${depth * 4}`}>
      {items.map(item => (
        <li key={item.id} className="py-0">
          {item.type === 'folder' ? (
            <div>
              <div 
                className="flex items-center py-1 hover:bg-gray-700 cursor-pointer"
                onClick={() => setCurrentFolder(currentFolder === item.id ? null : item.id)}
              >
                {/* Arrow Icon */}
                <span className="mr-1 text-gray-400">
                  {currentFolder === item.id ? (
                    <FaChevronDown size={12} />
                  ) : (
                    <FaChevronRight size={12} />
                  )}
                </span>
                
                {/* Folder Icon */}
                <span className="mr-2 text-blue-400">
                  {currentFolder === item.id ? <FaFolderOpen size={14} /> : <FaFolder size={14} />}
                </span>
                
                <span>{item.name}</span>
              </div>
              {currentFolder === item.id && (
                <div className="pl-4">
                  {renderFileTree(item.children || [], depth + 1)}
                  
                  {/* New File button inside folder */}
                  {!creatingItem && (
                    <button
                      className="text-xs text-gray-400 hover:text-white mt-1 flex items-center"
                      onClick={() => handleCreateItem('file', item.id)}
                    >
                      <FaPlus className="mr-1" size={10} /> New File
                    </button>
                  )}
                  
                  {/* File creation form inside folder */}
                  {creatingItem && newItemParentId === item.id && (
                    <div className="mb-2 flex mt-2">
                      <input
                        type="text"
                        value={newItemName}
                        onChange={(e) => setNewItemName(e.target.value)}
                        placeholder="New file name"
                        className="flex-1 bg-gray-700 text-white px-2 py-1 text-sm rounded-l outline-none"
                        autoFocus
                        onKeyDown={(e) => e.key === 'Enter' && handleSaveNewItem()}
                      />
                      <button 
                        className="bg-blue-600 px-2 rounded-r flex items-center justify-center"
                        onClick={handleSaveNewItem}
                      >
                        <FaCheck size={12} />
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div 
              className={`flex items-center hover:bg-gray-700 cursor-pointer ${activeFileId === item.id ? 'bg-gray-700' : ''}`}
              onClick={() => handleFileSelect(item.id)}
            >
              <span className="mr-2 text-gray-400">
                <FaFile size={12} />
              </span>
              <span>{item.name}</span>
            </div>
          )}
        </li>
      ))}
    </ul>
  );

  return (
    <div className="flex h-screen bg-gray-900 text-gray-200 font-sans">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 flex flex-col">
        <div className="p-3 border-b border-gray-700">
          <h2 className="font-semibold">EXPLORER</h2>
        </div>
        
        <div className="flex-1 overflow-y-auto p-2">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs uppercase text-gray-500">Vulcan-16</span>
            <div className="flex space-x-2">
              <button 
                className="text-gray-400 hover:text-white flex items-center"
                onClick={() => handleCreateItem('file')}
                title="New File"
              >
                <FaFile size={12} className="mr-1" />
                <FaPlus size={10} />
              </button>
              <button 
                className="text-gray-400 hover:text-white flex items-center"
                onClick={() => handleCreateItem('folder')}
                title="New Folder"
              >
                <FaFolder size={12} className="mr-1" />
                <FaPlus size={10} />
              </button>
            </div>
          </div>
          
          {/* Root level creation form */}
          {creatingItem && newItemParentId === null && (
            <div className="mb-2 flex">
              <input
                type="text"
                value={newItemName}
                onChange={(e) => setNewItemName(e.target.value)}
                placeholder={`New ${creatingItem} name`}
                className="flex-1 bg-gray-700 text-white px-2 py-1 text-sm rounded-l outline-none"
                autoFocus
                onKeyDown={(e) => e.key === 'Enter' && handleSaveNewItem()}
              />
              <button 
                className="bg-blue-600 px-2 rounded-r flex items-center justify-center"
                onClick={handleSaveNewItem}
              >
                <FaCheck size={12} />
              </button>
            </div>
          )}
          
          {renderFileTree(fileSystem)}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Tab Bar */}
        <div className="bg-gray-800 flex items-center border-b border-gray-700">
          <div className="flex overflow-x-auto">
            {openFiles.map(file => (
              <div 
                key={file.id}
                className={`py-2 px-4 flex items-center border-r border-gray-700 cursor-pointer ${
                  activeFileId === file.id ? 'bg-gray-900' : 'bg-gray-800 hover:bg-gray-750'
                }`}
                onClick={() => setActiveFileId(file.id)}
              >
                <span className="mr-2 text-gray-400">
                  <FaFile size={12} />
                </span>
                <span className="max-w-xs truncate">{file.name}</span>
                <button 
                  className="ml-2 text-gray-500 hover:text-white flex items-center"
                  onClick={(e) => handleCloseFile(file.id, e)}
                >
                  <FaTimes size={12} />
                </button>
              </div>
            ))}
          </div>
          
          <div className="ml-auto flex items-center px-4">
            <button
              onClick={handleCompile}
              disabled={isLoading || !activeFile}
              className={`p-2 rounded flex items-center justify-center ${
                isLoading 
                  ? 'text-gray-500' 
                  : activeFile 
                    ? 'text-green-400 hover:bg-gray-700' 
                    : 'text-gray-500'
              }`}
              title="Compile current file"
            >
              {isLoading ? (
                <FaSpinner className="animate-spin" size={16} />
              ) : (
                <FaPlay size={16} />
              )}
            </button>
          </div>
        </div>

        {/* Editor Area */}
        <div className="flex-1 flex">
          {activeFile ? (
            <textarea
              value={activeFile.content}
              onChange={(e) => handleFileContentChange(e.target.value)}
              className="w-full h-full bg-gray-900 text-gray-200 p-4 font-mono text-sm resize-none outline-none"
              spellCheck="false"
              placeholder={`// Start coding in ${activeFile.name.split('.').pop().toUpperCase()}...`}
            />
          ) : (
            <div className="flex items-center justify-center w-full h-full text-gray-500">
              <div className="text-center">
                <AiOutlineFile className="w-16 h-16 mx-auto mb-4 text-gray-600" />
                <p>Open a file from the explorer to start editing</p>
              </div>
            </div>
          )}
        </div>

        {/* Output Panel */}
        <div className="h-48 bg-gray-900 border-t border-gray-700 flex flex-col">
          <div className="bg-gray-800 px-4 py-2 text-sm text-gray-400">
            OUTPUT
          </div>
          <pre className="flex-1 p-4 overflow-auto bg-gray-900 text-green-400 font-mono text-sm">
            {output || '// Compilation output will appear here'}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default JackEditor;
