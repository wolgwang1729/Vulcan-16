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

const defaultMainJackCode = 
`
class Main {
    function void main() {
        var int userInput;
        var int randomNumber;
        var int counter;

        do Output.printString("                        Guess a number");
        do Output.println();
        do Output.println();
        do Output.println();
        do Output.printString("If you guess the number correctly, you win!");
        do Output.println();
        do Output.println();
        do Output.println();
        do Output.println();
        let counter = 0;
        let userInput = Keyboard.readInt("Enter a number between 0 and 10: ");
        do Output.println();
        do Output.println();
        do Output.println();
        do Output.println();
        do Output.printString("Are you ready for the verdict? Press enter to continue.");
        let counter = Main.measureTime();
        do Output.println();
        do Output.println();
        do Output.println();
        do Output.println();
        do Random.setSeed(counter);
		do Output.println();
        do Output.println();
        let randomNumber = Random.randRange(10);

        if (userInput = randomNumber) {
            do Output.printString("Congratulations! You guessed the number correctly!");
            do Output.println();
        } else {
            do Output.printString("Sorry, you guessed the number incorrectly.");
            do Output.println();
            do Output.println();
            do Output.printString("The correct number was: ");
            do Output.printInt(randomNumber);
        }
        return;
    }

    function int measureTime() {
        var int msCounter;
        var char input;
        var int key;
        let msCounter = 0;

        while (true) {
			do Sys.wait(1);
            let msCounter = msCounter + 1;
            let key= Keyboard.keyPressed();
			if(key=128) {
                    return msCounter;
                }
        }

        return msCounter;
    }
}
`
const defaultRandomJackCode = 
`
// Copyright 2012 Mark Armbrust. Permission granted for educational use.
/** Random.jack -- A not so random PRNG. */

class Random {
    static int seed;
    
    function void setSeed(int newSeed) {
        let seed = newSeed;
        return;
    }

    function int rand() {
        /** return a random number in the range 0..32767 */
        let seed = seed + 20251;
        if (seed < 0) {
            let seed = seed - 32767 - 1;
        }
        return seed;
    }

    function int randRange(int range) {
        /** return a random number in the range 0..range */
        var int mask;
        var int ret;
        let mask = 1;
        while (mask < range) {
            let mask = mask * 2 + 1;
        }
        let ret = Random.rand() & mask;
        while (ret > range) {
            let ret = Random.rand() & mask;
        }
        return ret;
    }

}
`


const JackCompiler = () => {
  const [fileSystem, setFileSystem] = useState([
    {
      id: 'folder-1',
      name: 'GuessANumber',
      type: 'folder',
      children: [
        { id: 'file-1', name: 'Main.jack', type: 'file', content: defaultMainJackCode },
        { id: 'file-2', name: 'Random.jack', type: 'file', content: defaultRandomJackCode },
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
  const [targetLanguage, setTargetLanguage] = useState('.hack');
  const [showDropdown, setShowDropdown] = useState(false);
  const [outputWidth, setOutputWidth] = useState(320); 
  const [isResizing, setIsResizing] = useState(false);

  const startResizing = () => setIsResizing(true);
  const stopResizing = () => setIsResizing(false);
  const resize = (e) => {
    if (isResizing) {
      const newWidth = window.innerWidth - e.clientX;
      // Constrain width between 100px and window width - 100px
      if (newWidth > 100 && newWidth < window.innerWidth - 100) {
        setOutputWidth(newWidth);
      }
    }
  };

  useEffect(() => {
    window.addEventListener('mouseup', stopResizing);
    window.addEventListener('mousemove', resize);
    return () => {
      window.removeEventListener('mouseup', stopResizing);
      window.removeEventListener('mousemove', resize);
    };
  }, [isResizing]);




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

  const findParentFolder = (fileId, items = fileSystem) => {
    for (const item of items) {
      if (item.type === 'folder' && item.children) {
        if (item.children.some(child => child.id === fileId)) {
          return item;
        }
      }
    }
    return null; 
  };

  const getAllFilesInFolder = (folder) => {
  let files = [];
  
  if (folder.children) {
    folder.children.forEach(child => {
        if (child.type === 'file') {
          files.push(child);
        } else if (child.type === 'folder') {
          files = files.concat(getAllFilesInFolder(child));
        }
      });
    }
  
    return files;
  };


  const activeFile = findFile(activeFileId);

  const handleFileSelect = (fileId) => {
    const file = findFile(fileId);
    if (!file) return;

    setActiveFileId(fileId);
    
    if (!openFiles.some(f => f.id === fileId)) {
      setOpenFiles([...openFiles, file]);
    }
  };

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
    
    setOpenFiles(openFiles.map(file => 
      file.id === activeFileId ? { ...file, content } : file
    ));
  };

  const handleCloseFile = (fileId, e) => {
    e.stopPropagation();
    const newOpenFiles = openFiles.filter(file => file.id !== fileId);
    setOpenFiles(newOpenFiles);
    
    if (activeFileId === fileId) {
      setActiveFileId(newOpenFiles.length > 0 ? newOpenFiles[0].id : null);
    }
  };

  const handleCreateItem = (type, parentId = null) => {
    setCreatingItem(type);
    setNewItemParentId(parentId);
    setNewItemName('');
  };

  const handleSaveNewItem = () => {
    if (!newItemName.trim()) {
      setCreatingItem(null);
      setNewItemParentId(null);
      return;
    }

    if (creatingItem === 'file') {
      const allowedExtensions = ['asm', 'vm', 'jack'];
      const fileName = newItemName.trim();
      
      if (!fileName.includes('.')) {
        setOutput('Error: File must have an extension (.asm, .vm, or .jack)');
        return;
      }
      
      const extension = fileName.split('.').pop().toLowerCase();
      
      if (!allowedExtensions.includes(extension)) {
        setOutput(`Error: Only .asm, .vm, and .jack files are allowed. You tried to create: .${extension}`);
        return;
      }
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

  const getTargetOptions = () => {
    if (!activeFile) return [];
    const ext = activeFile.name.split('.').pop();
    switch (ext) {
      case 'asm':  return ['.hack'];
      case 'vm':   return ['.asm', '.hack'];
      case 'jack': return ['.vm', '.asm', '.hack'];
      default:     return ['.hack'];
    }
  };

  const handleSelectTarget = (lang) => {
    setTargetLanguage(lang);
    setShowDropdown(false);
  };

  const handleCompile = async () => {
    if (!activeFile || isLoading) return;

    setIsLoading(true);
    setOutput('Compiling...');

    try {
      const extension = activeFile.name.split('.').pop();
      let language;

      switch (extension) {
        case 'asm': language = 'assembly'; break;
        case 'jack': language = 'jack'; break;
        case 'vm': language = 'vm'; break;
        default:
          setOutput(`Error: Unsupported file type (.${extension})`);
          setIsLoading(false);
          return;
      }

      const parentFolder = findParentFolder(activeFileId);

      // Validation check for .asm and .vm files - they must be outside folders
      if ((language === 'assembly' || language === 'vm') && parentFolder) {
        setOutput('Error: .asm and .vm files must be compiled outside of folders. Please move this file to the root level first.');
        setIsLoading(false);
        return;
      }

      // Validation check for .jack files - they must be inside folders
      if (language === 'jack' && !parentFolder) {
        setOutput('Error: .jack files can only be compiled when placed inside a folder. Please move this file to a folder first.');
        setIsLoading(false);
        return;
      }

      const formData = new FormData();
      formData.append('language', language);
      formData.append('target', targetLanguage); // Add target language to the request

      if (parentFolder && (language === 'jack' || language === 'vm')) {
        // File is inside a folder - send entire folder
        const folderFiles = getAllFilesInFolder(parentFolder);
        
        formData.append('folder_name', parentFolder.name);
        formData.append('is_folder', 'true');
        
        // Add all files in the folder
        folderFiles.forEach((file, index) => {
          const blob = new Blob([file.content], { type: 'text/plain' });
          const fileObj = new File([blob], file.name, { type: 'text/plain' });
          formData.append(`files`, fileObj);
        });
        
        setOutput(`Compiling folder: ${parentFolder.name}...`);
      } else {
        // Single file compilation
        const blob = new Blob([activeFile.content], { type: 'text/plain' });
        const file = new File([blob], activeFile.name, { type: 'text/plain' });
        
        formData.append('file', file);
        formData.append('is_folder', 'false');
        formData.append('target', targetLanguage); 
      }

      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/compile`, {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      
      if (result.success) {
        setOutput(result.hack_code || result.asm_code || 'Compilation successful');
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
                className="flex items-center pl-2 py-1 hover:bg-gray-700 cursor-pointer"
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
                    <div 
                      className='flex pl-2 py-0.5 items-center hover:bg-gray-700 cursor-pointer'
                      onClick={() => handleCreateItem('file', item.id)}
                    >
                      <div
                        className="text-xs text-gray-400 mt-1 flex items-center"
                      >
                        <FaPlus className="mr-1" size={10} /> New File
                      </div>
                    </div>
                  )}
                  
                  {/* File creation form inside folder */}
                  {creatingItem && newItemParentId === item.id && (
                    <div className="mb-0 flex mt-1">
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
              className={`flex pl-2 py-0.5 items-center cursor-pointer ${
                activeFileId === item.id ? 'bg-blue-800 border border-blue-500' : 'hover:bg-gray-700 bg-gray-800'
              }`}
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
        
        <div className="flex-1 overflow-y-auto">
          <div className="flex justify-between items-center mb-2 p-1">
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
            <div className="relative flex items-center hover:bg-gray-800 hover:rounded-sm">
              {/* Play button - no border */}
              <button
                onClick={handleCompile}
                disabled={isLoading || !activeFile}
                className={`p-2 rounded flex items-center justify-center
                            ${isLoading
                              ? 'text-gray-500'
                              : activeFile
                                  ? 'text-green-400 hover:bg-gray-700'
                                  : 'text-gray-500'}`}
                title={`Compile → ${targetLanguage}`}
              >
                {isLoading ? (
                  <FaSpinner className="animate-spin" size={16} />
                ) : (
                  <FaPlay size={16} />
                )}
              </button>

              {/* Arrow button - only show when file is NOT inside a folder */}
              {activeFile && !findParentFolder(activeFileId) && (
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className="p-2 rounded flex items-center justify-center
                             text-gray-400 hover:text-white hover:bg-gray-700"
                  title="Select target language"
                >
                  <FaChevronDown size={12} />
                </button>
              )}

              {/* Dropdown */}
              {showDropdown && (
                <div
                  className="absolute right-0 mt-1 w-32 bg-gray-800 border border-gray-700
                             rounded shadow-lg z-10"
                  style={{ top: '100%' }}
                >
                  {/* Target Language Header */}
                  <div className="px-2 py-1 text-xs text-gray-400 bg-gray-900 border-b border-gray-600">
                    Target Language
                  </div>
                  
                  {/* Language Options */}
                  {getTargetOptions().map(lang => (
                    <div
                      key={lang}
                      onClick={() => handleSelectTarget(lang)}
                      className={`px-2 py-1 cursor-pointer 
                                  ${targetLanguage === lang ? 'bg-blue-600' : 'hover:bg-gray-700'}`}
                    >
                      {lang}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
        {/* Editor and Output Container */}
        <div className="flex-1 flex" style={{ 
          position: 'relative', 
          maxHeight: 'calc(100vh - 50px)' 
        }}>
          {/* Editor Area */}
          <div style={{ flex: 1, minWidth: 100 }} className="flex flex-col">
            {activeFile ? (
              <textarea
                value={activeFile.content}
                onChange={(e) => handleFileContentChange(e.target.value)}
                className="w-full flex-1 bg-gray-900 text-gray-200 p-4 font-mono text-sm resize-none outline-none overflow-y-auto"
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

          {/* Resizable Divider */}
          <div
            onMouseDown={startResizing}
            className="bg-gray-700 hover:bg-gray-600 cursor-col-resize"
            style={{ 
              width: 4, 
              cursor: 'col-resize', 
              userSelect: 'none',
              transition: 'background-color 0.2s'
            }}
          />

          {/* Output Panel */}
          <div 
            style={{ 
              width: outputWidth, 
              minWidth: 100, 
              backgroundColor: '#1a202c' 
            }} 
            className="flex flex-col border-l border-gray-700"
          >
            <div className="bg-gray-800 px-4 py-2 text-sm text-gray-400 border-b border-gray-700">
              OUTPUT
            </div>
            <pre className="flex-1 p-4 overflow-auto bg-gray-900 text-green-400 font-mono text-sm">
              {output || '//Compilation output will appear here'}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JackCompiler;
