import React, { useState, useEffect, useRef } from 'react';
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
  FaChevronDown,
  FaStop,
  FaStepForward
} from 'react-icons/fa';
import { AiOutlineFile } from 'react-icons/ai';

const rectangleHack = 
`0100000000000000
1110110000010000
0000000000010000
1110001100001000
0000000000100000
1110110000010000
0000000000010001
1110001100001000
0000000000010010
1110101010001000
1110101010010000
0000000000000000
1111110000010000
0000000000010011
1110001100001000
0000000000100000
1110001100000110
0000000000010000
1111110000010000
0000000000010010
1111000010010000
1110001100100000
1110111010001000
0000000000010001
1111110000010000
0000000000010010
1111000010001000
0000000000010011
1111110010001000
1111110000010000
0000000000010001
1110001100000001
0000000000100000
1110101010000111`;

const addHack =
`0000000000000000
1111110000010000
0000000000000001
1111000010010000
0000000000000010
1110001100001000
0000000000000110
1110101010000111`;

// Screen Component
const Screen = ({ memory, isRunning }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Clear screen
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, 512, 256);
    
    if (!isRunning) return;

    // Draw pixels based on screen memory (16384 to 24575)
    ctx.fillStyle = 'black';
    
    for (let row = 0; row < 256; row++) {
      for (let col = 0; col < 32; col++) { // 32 words per row (512 pixels / 16 bits)
        const memoryAddress = 16384 + (row * 32) + col;
        const word = memory[memoryAddress] || 0;
        
        // Draw 16 pixels from this word
        for (let bit = 0; bit < 16; bit++) {
          if ((word >> (15 - bit)) & 1) {
            const x = col * 16 + bit;
            const y = row;
            ctx.fillRect(x, y, 1, 1);
          }
        }
      }
    }
  }, [memory, isRunning]);

  return (
    <div className="bg-white border border-gray-400 p-2 mb-2">
      <div className="text-xs text-gray-600 mb-1">Screen (512x256)</div>
      <canvas 
        ref={canvasRef}
        width={512}
        height={256}
        className="border border-gray-300"
        style={{ maxWidth: '100%', height: 'auto' }}
      />
    </div>
  );
};

// Key Display Component with Toggle
const KeyDisplay = ({ currentKey, pcKeyboardEnabled, setPcKeyboardEnabled, isRunning }) => {
  const getKeyName = (keyCode) => {
    if (!keyCode) return 'None';
    if (keyCode === 32) return 'SPACE';
    if (keyCode === 13) return 'ENTER';
    if (keyCode >= 65 && keyCode <= 90) return String.fromCharCode(keyCode);
    if (keyCode >= 48 && keyCode <= 57) return String.fromCharCode(keyCode);
    return `Key(${keyCode})`;
  };

  return (
    <div className="bg-gray-800 p-3 rounded">
      <div className="text-xs text-gray-400 mb-2 flex justify-between items-center">
        <span>PC Keyboard Input</span>
        <button
          onClick={() => setPcKeyboardEnabled(!pcKeyboardEnabled)}
          className={`px-2 py-1 text-xs rounded ${
            pcKeyboardEnabled 
              ? 'bg-green-600 text-white hover:bg-green-700' 
              : 'bg-gray-600 text-gray-300 hover:bg-gray-500'
          }`}
          title={pcKeyboardEnabled ? 'Disable PC Keyboard' : 'Enable PC Keyboard'}
        >
          {pcKeyboardEnabled ? 'ON' : 'OFF'}
        </button>
      </div>
      
      <div className="text-center">
        <div className="text-xs text-gray-500 mb-1">Current Key:</div>
        <div className={`text-2xl font-bold px-4 py-2 rounded ${
          currentKey && pcKeyboardEnabled && isRunning
            ? 'bg-blue-600 text-white' 
            : 'bg-gray-700 text-gray-400'
        }`}>
          {pcKeyboardEnabled && isRunning ? getKeyName(currentKey) : 'OFF'}
        </div>
        {currentKey && pcKeyboardEnabled && isRunning && (
          <div className="text-xs text-gray-500 mt-1">
            Code: {currentKey}
          </div>
        )}
      </div>
      
      <div className="text-xs text-gray-500 mt-2 text-center">
        {pcKeyboardEnabled 
          ? isRunning 
            ? 'Press any key on your keyboard'
            : 'Start simulation to use keyboard'
          : 'Toggle ON to enable keyboard input'
        }
      </div>
    </div>
  );
};

// CPU Registers Component
const CpuRegisters = ({ aRegister, dRegister, pc, cycles }) => {
  return (
    <div className="bg-gray-800 p-2 mb-2 rounded">
      <div className="text-xs text-gray-400 mb-1">CPU Registers</div>
      <div className="grid grid-cols-4 gap-2 text-center">
        <div className="bg-gray-700 p-2 rounded">
          <div className="text-xs text-gray-500">A Register</div>
          <div className="text-lg font-semibold">{aRegister}</div>
        </div>
        <div className="bg-gray-700 p-2 rounded">
          <div className="text-xs text-gray-500">D Register</div>
          <div className="text-lg font-semibold">{dRegister}</div>
        </div>
        <div className="bg-gray-700 p-2 rounded">
          <div className="text-xs text-gray-500">Program Counter</div>
          <div className="text-lg font-semibold">{pc}</div>
        </div>
        <div className="bg-gray-700 p-2 rounded">
          <div className="text-xs text-gray-500">Cycles</div>
          <div className="text-lg font-semibold">{cycles}</div>
        </div>
      </div>
    </div>
  );
};

// RAM Editor Component
const RamEditor = ({ memory, setMemory, isRunning }) => {
  const [selectedAddress, setSelectedAddress] = useState(0);
  const [newValue, setNewValue] = useState(0);

  const handleAddressChange = (e) => {
    const address = parseInt(e.target.value, 10);
    if (!isNaN(address) && address >= 0 && address < 24577) {
      setSelectedAddress(address);
      setNewValue(memory[address] || 0);
    }
  };

  const handleValueChange = (e) => {
    const value = parseInt(e.target.value, 10);
    if (!isNaN(value) && value >= -32768 && value <= 32767) {
      setNewValue(value);
    }
  };

  const handleSave = () => {
    if (selectedAddress >= 0 && selectedAddress < 24577) {
      setMemory(prev => {
        const newMemory = [...prev];
        newMemory[selectedAddress] = newValue & 0xFFFF;
        return newMemory;
      });
    }
  };

  return (
    <div className="bg-gray-800 p-3 mb-2 rounded">
      <div className="text-xs text-gray-400 mb-2">RAM Editor (0 - 24576)</div>
      
      <div className="grid grid-cols-1 gap-2 mb-2">
        <div className="flex gap-2">
          <input
            type="number"
            value={selectedAddress}
            onChange={handleAddressChange}
            min="0"
            max="24576"
            className="bg-gray-700 text-white px-3 py-1 text-sm rounded outline-none flex-1"
            placeholder="Address"
            disabled={isRunning}
          />
          <input
            type="number"
            value={newValue}
            onChange={handleValueChange}
            min="-32768"
            max="32767"
            className="bg-gray-700 text-white px-3 py-1 text-sm rounded outline-none flex-1"
            placeholder="Value"
            disabled={isRunning}
          />
          <button
            onClick={handleSave}
            className="bg-blue-600 px-3 py-1 text-sm rounded flex items-center justify-center hover:bg-blue-700"
            disabled={isRunning}
          >
            <FaCheck size={12} />
          </button>
        </div>
      </div>
      
      <div className="text-xs text-gray-500 mb-2">
        Current value at {selectedAddress}: <span className="text-white">{memory[selectedAddress] || 0}</span>
      </div>
      
      <div className="text-xs text-gray-500">
        Special addresses: Screen (16384-24575), Keyboard (24576)
      </div>
    </div>
  );
};

const HardwareSimulator = () => {
  const [fileSystem, setFileSystem] = useState([
    {
      id: 'file-rectangle',
      name: 'Rectangle.hack',
      type: 'file',
      content: rectangleHack,
    },
    {
      id: 'file-add',
      name: 'Add.hack',
      type: 'file',
      content: addHack,
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
  const [outputWidth, setOutputWidth] = useState(400); 
  const [isResizing, setIsResizing] = useState(false);
  const [editorWidth, setEditorWidth] = useState(null);

  // Hardware simulation state
  const [isRunning, setIsRunning] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [rom, setRom] = useState(new Array(32768).fill(0));
  const [memory, setMemory] = useState(new Array(24577).fill(0));
  const [pc, setPc] = useState(0);
  const [aRegister, setARegister] = useState(0);
  const [dRegister, setDRegister] = useState(0);
  const [currentKey, setCurrentKey] = useState(0);
  const [cycles, setCycles] = useState(0);
  const [pcKeyboardEnabled, setPcKeyboardEnabled] = useState(false);

  const simulationRef = useRef(null);

  // PC Keyboard Event Listeners with Toggle
  useEffect(() => {
    // Only add event listeners if PC keyboard is enabled AND simulation is running
    if (!pcKeyboardEnabled || !isRunning) {
      return;
    }

    const handleKeyDown = (e) => {
      // Only capture keys when NOT focused on input fields or textarea
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        return;
      }
      
      e.preventDefault();
      
      let keyCode = 0;
      
      if (e.key === ' ') {
        keyCode = 32; // Space
      } else if (e.key === 'Enter') {
        keyCode = 128; // Enter
      } else if (e.key.length === 1) {
        keyCode = e.key.toUpperCase().charCodeAt(0);
      }
      
      if (keyCode > 0) {
        setCurrentKey(keyCode);
      }
    };

    const handleKeyUp = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        return;
      }
      
      e.preventDefault();
      setTimeout(() => setCurrentKey(0), 100);
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [pcKeyboardEnabled, isRunning]);

  // Initialize memory mapping
  useEffect(() => {
    setMemory(prev => {
      const newMemory = [...prev];
      newMemory[24576] = currentKey;
      return newMemory;
    });
  }, [currentKey]);

  // AUTO-RESIZE WHEN .hack FILE IS SELECTED
  useEffect(() => {
    const activeFile = findFile(activeFileId);
    if (activeFile && activeFile.name.endsWith('.hack')) {
      const charWidth = 8;
      const hackEditorWidth = (16 * charWidth) + 50;
      setEditorWidth(hackEditorWidth);
      setOutputWidth(window.innerWidth - 256 - hackEditorWidth - 10);
    } else {
      setEditorWidth(null);
      setOutputWidth(400);
    }
  }, [activeFileId]);

  const startResizing = () => setIsResizing(true);
  const stopResizing = () => setIsResizing(false);
  const resize = (e) => {
    if (isResizing) {
      const newWidth = window.innerWidth - e.clientX;
      if (newWidth > 200 && newWidth < window.innerWidth - 200) {
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

// CPU simulation logic
const executeInstruction = (instruction) => {
  if ((instruction & 0b1000000000000000) === 0) {
    // A-instruction: @value
    const value = instruction & 0b0111111111111111;
    setARegister(value);
  } else {
    // C-instruction
    const comp = (instruction >> 6) & 0b1111111;
    const dest = (instruction >> 3) & 0b111;
    const jump = instruction & 0b111;

    let aluResult = 0;
    const aValue = memory[aRegister] || 0;
    const dValue = dRegister;

    // ALU computation based on comp bits
    switch (comp) {
      case 0b0101010:
        aluResult = 0;
        break; // 0
      case 0b0111111:
        aluResult = 1;
        break; // 1
      case 0b0111010:
        aluResult = -1;
        break; // -1
      case 0b0001100:
        aluResult = dValue;
        break; // D
      case 0b0110000:
        aluResult = aRegister;
        break; // A
      case 0b1110000:
        aluResult = aValue;
        break; // M
      case 0b0001101:
        aluResult = ~dValue;
        break; // !D
      case 0b0110001:
        aluResult = ~aRegister;
        break; // !A
      case 0b1110001:
        aluResult = ~aValue;
        break; // !M
      case 0b0001111:
        aluResult = -dValue;
        break; // -D
      case 0b0110011:
        aluResult = -aRegister;
        break; // -A
      case 0b1110011:
        aluResult = -aValue;
        break; // -M
      case 0b0011111:
        aluResult = dValue + 1;
        break; // D+1
      case 0b0110111:
        aluResult = aRegister + 1;
        break; // A+1
      case 0b1110111:
        aluResult = aValue + 1;
        break; // M+1
      case 0b0001110:
        aluResult = dValue - 1;
        break; // D-1
      case 0b0110010:
        aluResult = aRegister - 1;
        break; // A-1
      case 0b1110010:
        aluResult = aValue - 1;
        break; // M-1
      case 0b0000010:
        aluResult = dValue + aRegister;
        break; // D+A
      case 0b1000010:
        aluResult = dValue + aValue;
        break; // D+M
      case 0b0010011:
        aluResult = dValue - aRegister;
        break; // D-A
      case 0b1010011:
        aluResult = dValue - aValue;
        break; // D-M
      case 0b0000111:
        aluResult = aRegister - dValue;
        break; // A-D
      case 0b1000111:
        aluResult = aValue - dValue;
        break; // M-D
      case 0b0000000:
        aluResult = dValue & aRegister;
        break; // D&A
      case 0b1000000:
        aluResult = dValue & aValue;
        break; // D&M
      case 0b0010101:
        aluResult = dValue | aRegister;
        break; // D|A
      case 0b1010101:
        aluResult = dValue | aValue;
        break; // D|M
      default:
        aluResult = 0;
    }
    
    // Normalize to 16-bit signed integer for comparison
    const signedAluResult = (aluResult << 16) >> 16;
    
    // Handle destinations
    if (dest & 0b100) {
      // A register
      setARegister(aluResult & 0b1111111111111111);
    }
    if (dest & 0b010) {
      // D register
      setDRegister(aluResult & 0b1111111111111111);
    }
    if (dest & 0b001) {
      // Memory
      setMemory((prev) => {
        const newMemory = [...prev];
        if (aRegister < 24577) {
          newMemory[aRegister] = aluResult & 0b1111111111111111;
        }
        return newMemory;
      });
    }

    // Handle jumps
    const isZero = signedAluResult === 0;
    const isNeg = signedAluResult < 0;
    const isPos = signedAluResult > 0;

    let shouldJump = false;
    switch (jump) {
      case 0b001:
        shouldJump = isPos;
        break; // JGT
      case 0b010:
        shouldJump = isZero;
        break; // JEQ
      case 0b011:
        shouldJump = isPos || isZero;
        break; // JGE
      case 0b100:
        shouldJump = isNeg;
        break; // JLT
      case 0b101:
        shouldJump = !isZero;
        break; // JNE
      case 0b110:
        shouldJump = isNeg || isZero;
        break; // JLE
      case 0b111:
        shouldJump = true;
        break; // JMP
    }

    if (shouldJump) {
      setPc(aRegister);
      return;
    }
  }

  setPc((prev) => (prev + 1) % 32768);
};

// Simulation loop
useEffect(() => {
  if (!isRunning || isPaused) {
    if (simulationRef.current) {
      clearInterval(simulationRef.current);
      simulationRef.current = null;
    }
    return;
  }

  simulationRef.current = setInterval(() => {
    if (pc < rom.length && rom[pc] !== undefined) {
      executeInstruction(rom[pc]);
      setCycles((prev) => prev + 1);
    }
  }, 10); // 100 Hz simulation

  return () => {
    if (simulationRef.current) {
      clearInterval(simulationRef.current);
    }
  };
}, [isRunning, isPaused, pc, rom, aRegister, dRegister, memory]);

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

  useEffect(() => {
    if (!activeFile) return;
    
    if (activeFile.name.endsWith('.hack')) {
      try {
        const lines = activeFile.content.trim().split('\n');
        const newRom = new Array(32768).fill(0);
        
        lines.forEach((line, index) => {
          if (index < 32768 && line.trim()) {
            newRom[index] = parseInt(line.trim(), 2);
          }
        });
        
        setRom(newRom);
        setPc(0);
        setARegister(0);
        setDRegister(0);
        setCycles(0);
        setOutput('Loaded .hack file into ROM. Ready to run.');
      } catch (error) {
        setOutput(`Error loading .hack file: ${error.message}`);
      }
    }
  }, [activeFileId, activeFile?.content]);

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
      const allowedExtensions = ['asm', 'vm', 'jack', 'hack'];
      const fileName = newItemName.trim();
      
      if (!fileName.includes('.')) {
        setOutput('Error: File must have an extension (.asm, .vm, .jack, or .hack)');
        return;
      }
      
      const extension = fileName.split('.').pop().toLowerCase();
      
      if (!allowedExtensions.includes(extension)) {
        setOutput(`Error: Only .asm, .vm, .jack, and .hack files are allowed. You tried to create: .${extension}`);
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

  const handleRunStop = async () => {
    if (!activeFile) return;

    const extension = activeFile.name.split('.').pop();

    if (extension === 'hack') {
      if (isRunning) {
        setIsRunning(false);
        setIsPaused(false);
        setPcKeyboardEnabled(false); // Disable PC keyboard when stopping
        setOutput('Simulation stopped');
      } else {
        try {
          setIsRunning(true);
          setIsPaused(false);
          setOutput('Hardware simulation started\nLoaded program into ROM\nScreen active\nToggle PC Keyboard ON in the panel to use keyboard input');
        } catch (error) {
          setOutput(`Error loading .hack file: ${error.message}`);
        }
      }
    } else {
      handleCompile();
    }
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
        case 'hack': 
          setOutput('Note: .hack files are already compiled machine code. Use Run to simulate.');
          setIsLoading(false);
          return;
        default:
          setOutput(`Error: Unsupported file type (.${extension})`);
          setIsLoading(false);
          return;
      }

      const parentFolder = findParentFolder(activeFileId);

      if ((language === 'assembly' || language === 'vm') && parentFolder) {
        setOutput('Error: .asm and .vm files must be compiled outside of folders.');
        setIsLoading(false);
        return;
      }

      if (language === 'jack' && !parentFolder) {
        setOutput('Error: .jack files can only be compiled when placed inside a folder.');
        setIsLoading(false);
        return;
      }

      const formData = new FormData();
      formData.append('language', language);
      formData.append('target', targetLanguage);

      if (parentFolder && (language === 'jack' || language === 'vm')) {
        const folderFiles = getAllFilesInFolder(parentFolder);
        
        formData.append('folder_name', parentFolder.name);
        formData.append('is_folder', 'true');
        
        folderFiles.forEach((file, index) => {
          const blob = new Blob([file.content], { type: 'text/plain' });
          const fileObj = new File([blob], file.name, { type: 'text/plain' });
          formData.append(`files`, fileObj);
        });
        
        setOutput(`Compiling folder: ${parentFolder.name}...`);
      } else {
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
                <span className="mr-1 text-gray-400">
                  {currentFolder === item.id ? (
                    <FaChevronDown size={12} />
                  ) : (
                    <FaChevronRight size={12} />
                  )}
                </span>
                
                <span className="mr-2 text-blue-400">
                  {currentFolder === item.id ? <FaFolderOpen size={14} /> : <FaFolder size={14} />}
                </span>
                
                <span>{item.name}</span>
              </div>
              {currentFolder === item.id && (
                <div className="pl-4">
                  {renderFileTree(item.children || [], depth + 1)}
                  
                  {!creatingItem && (
                    <div 
                      className='flex pl-2 py-0.5 items-center hover:bg-gray-700 cursor-pointer'
                      onClick={() => handleCreateItem('file', item.id)}
                    >
                      <div className="text-xs text-gray-400 mt-1 flex items-center">
                        <FaPlus className="mr-1" size={10} /> New File
                      </div>
                    </div>
                  )}
                  
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
            <div className="relative flex items-center">
              <button
                onClick={handleRunStop}
                disabled={isLoading || !activeFile}
                className={`p-2 rounded flex items-center justify-center mr-2
                            ${isLoading
                              ? 'text-gray-500'
                              : activeFile
                                  ? isRunning && activeFile.name.endsWith('.hack')
                                    ? 'text-red-400 hover:bg-gray-700'
                                    : 'text-green-400 hover:bg-gray-700'
                                  : 'text-gray-500'}`}
                title={activeFile && activeFile.name.endsWith('.hack') 
                  ? (isRunning ? 'Stop Simulation' : 'Run Simulation')
                  : `Compile → ${targetLanguage}`}
              >
                {isLoading ? (
                  <FaSpinner className="animate-spin" size={16} />
                ) : isRunning && activeFile && activeFile.name.endsWith('.hack') ? (
                  <FaStop size={16} />
                ) : (
                  <FaPlay size={16} />
                )}
              </button>

              {activeFile && !findParentFolder(activeFileId) && 
                activeFile.name.split('.').pop() !== 'hack' && (
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className="p-2 rounded flex items-center justify-center
                             text-gray-400 hover:text-white hover:bg-gray-700"
                  title="Select target language"
                >
                  <FaChevronDown size={12} />
                </button>
              )}

              {showDropdown && (
                <div
                  className="absolute right-0 mt-1 w-32 bg-gray-800 border border-gray-700
                             rounded shadow-lg z-10"
                  style={{ top: '100%' }}
                >
                  <div className="px-2 py-1 text-xs text-gray-400 bg-gray-900 border-b border-gray-600">
                    Target Language
                  </div>
                  
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
          <div 
            style={{ 
              width: editorWidth || 'auto',
              flex: editorWidth ? '0 0 auto' : 1,
              minWidth: 100 
            }} 
            className="flex flex-col"
          >
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
          {!editorWidth && (
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
          )}

          {/* Output Panel */}
          <div 
            style={{ 
              width: outputWidth, 
              minWidth: 200, 
              backgroundColor: '#1a202c' 
            }} 
            className="flex flex-col border-l border-gray-700"
          >
            <div className="bg-gray-800 px-4 py-2 text-sm text-gray-400 border-b border-gray-700 flex justify-between">
              <span>
                {activeFile && activeFile.name.endsWith('.hack') 
                  ? `HARDWARE SIMULATOR (PC: ${pc}, Cycles: ${cycles})` 
                  : 'OUTPUT'}
              </span>
              {isRunning && (
                <span className={`text-xs ${isPaused ? 'text-yellow-400' : 'text-green-400'}`}>
                  {isPaused ? 'PAUSED' : 'RUNNING'}
                </span>
              )}
            </div>
            
            {activeFile && activeFile.name.endsWith('.hack') ? (
              <div className="flex-1 flex overflow-hidden">
                {/* Left column - CPU and RAM */}
                <div className="flex-1 overflow-y-auto p-2">
                  <CpuRegisters 
                    aRegister={aRegister} 
                    dRegister={dRegister} 
                    pc={pc} 
                    cycles={cycles} 
                  />
                  
                  <RamEditor 
                    memory={memory} 
                    setMemory={setMemory} 
                    isRunning={isRunning} 
                  />
                </div>
                
                {/* Right column - Screen and Key Display */}
                <div className="flex-1 flex flex-col p-2">
                  <Screen memory={memory} isRunning={isRunning} />
                  <KeyDisplay 
                    currentKey={currentKey} 
                    pcKeyboardEnabled={pcKeyboardEnabled}
                    setPcKeyboardEnabled={setPcKeyboardEnabled}
                    isRunning={isRunning}
                  />
                </div>
              </div>
            ) : (
              <pre className="flex-1 p-4 overflow-auto bg-gray-900 text-green-400 font-mono text-sm">
                {output || '//Compilation output will appear here\n//Run .hack files to start hardware simulation\n//Toggle PC Keyboard ON when running to use keyboard input'}
              </pre>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HardwareSimulator;
