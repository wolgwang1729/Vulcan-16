import { render, screen, fireEvent, waitFor, within } from '@testing-library/react'
import { vi } from 'vitest'
import HardwareSimulator from './HardwareSimulator'

describe('HardwareSimulator', () => {
  let nowCounter = 0

  const mockCanvasContext = {
    fillStyle: '',
    fillRect: vi.fn(),
  }

  const createRootItem = async (type, name) => {
    fireEvent.click(screen.getByTitle(type === 'file' ? 'New File' : 'New Folder'))
    const input = await screen.findByPlaceholderText(`New ${type} name`)
    fireEvent.change(input, { target: { value: name } })
    const saveButton = input.parentElement.querySelector('button')
    expect(saveButton).not.toBeNull()
    fireEvent.click(saveButton)
  }

  const openHackFile = async (name = 'Rectangle.hack') => {
    fireEvent.click(screen.getAllByText(name)[0])
    await screen.findByText(/HARDWARE SIMULATOR/)
  }

  const createFileInFolder = async (folderName, fileName) => {
    const folder = screen.getByText(folderName)
    if (!screen.queryByText('New File')) {
      fireEvent.click(folder)
    }

    fireEvent.click(screen.getByText('New File'))
    const nestedInput = await screen.findByPlaceholderText('New file name')
    fireEvent.change(nestedInput, { target: { value: fileName } })
    fireEvent.keyDown(nestedInput, { key: 'Enter' })
    await screen.findByText(fileName)
  }

  const setRamValue = async (address, value) => {
    const [addressInput, valueInput] = screen.getAllByRole('spinbutton')

    fireEvent.change(addressInput, { target: { value: String(address) } })
    await waitFor(() => {
      expect(screen.getByText(new RegExp(`Current value at ${address}:`))).toBeInTheDocument()
    })

    fireEvent.change(valueInput, { target: { value: String(value) } })
    fireEvent.click(valueInput.parentElement.querySelector('button'))

    const expectedStoredValue = value & 0xFFFF
    await waitFor(() => {
      expect(screen.getByText(new RegExp(`Current value at ${address}:`)).textContent).toContain(String(expectedStoredValue))
    })
  }

  const openFileByName = async (name) => {
    fireEvent.click(screen.getAllByText(name)[0])
    await screen.findByDisplayValue(/.*/)
  }

  const createDeferred = () => {
    let resolve
    const promise = new Promise((res) => {
      resolve = res
    })
    return { promise, resolve }
  }

  beforeEach(() => {
    nowCounter = 1000
    vi.spyOn(Date, 'now').mockImplementation(() => {
      nowCounter += 1
      return nowCounter
    })

    Object.defineProperty(HTMLCanvasElement.prototype, 'getContext', {
      configurable: true,
      value: () => mockCanvasContext,
    })

    vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it('renders initial explorer and empty editor state', () => {
    render(<HardwareSimulator />)

    expect(screen.getByText('EXPLORER')).toBeInTheDocument()
    expect(screen.getByText('Rectangle.hack')).toBeInTheDocument()
    expect(screen.getByText('Add.hack')).toBeInTheDocument()
    expect(screen.getByText('Multiplication.hack')).toBeInTheDocument()
    expect(screen.getByText('Open a file from the explorer to start editing')).toBeInTheDocument()
  })

  it('opens a .hack file and shows simulator panels', async () => {
    render(<HardwareSimulator />)

    await openHackFile()

    expect(screen.getByText(/HARDWARE SIMULATOR \(PC: 0, Cycles: 0\)/)).toBeInTheDocument()
    expect(screen.getByText('CPU Registers')).toBeInTheDocument()
    expect(screen.getByText('RAM Editor (0 - 24576)')).toBeInTheDocument()
    expect(screen.getByText('PC Keyboard Input')).toBeInTheDocument()
    expect(screen.getByTitle('Run Simulation')).toBeInTheDocument()
  })

  it('renders output mode for non-hack files', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'Program.asm')
    await openFileByName('Program.asm')

    expect(screen.getByText('OUTPUT')).toBeInTheDocument()
    expect(screen.getByText(/Compilation output will appear here/)).toBeInTheDocument()
    expect(screen.getByTitle('Compile → .hack')).toBeInTheDocument()
  })

  it('toggles run state for a .hack simulation', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    fireEvent.click(screen.getByTitle('Run Simulation'))

    expect(await screen.findByText('RUNNING')).toBeInTheDocument()
    expect(screen.getByTitle('Stop Simulation')).toBeInTheDocument()

    fireEvent.click(screen.getByTitle('Stop Simulation'))

    await waitFor(() => {
      expect(screen.queryByText('RUNNING')).not.toBeInTheDocument()
    })
    expect(screen.getByTitle('Run Simulation')).toBeInTheDocument()
  })

  it('advances cycles while simulation is running', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Add.hack')
    fireEvent.click(screen.getByTitle('Run Simulation'))

    await waitFor(() => {
      expect(screen.getByText(/Cycles: [1-9]\d*/)).toBeInTheDocument()
    }, { timeout: 2000 })
  })

  it('resets cpu registers and cycles when opening another .hack file', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Add.hack')
    fireEvent.click(screen.getByTitle('Run Simulation'))

    await waitFor(() => {
      expect(screen.getByText(/Cycles: [1-9]\d*/)).toBeInTheDocument()
    })

    fireEvent.click(screen.getAllByText('Rectangle.hack')[0])

    await waitFor(() => {
      expect(screen.getByText(/HARDWARE SIMULATOR \(PC: 0, Cycles: 0\)/)).toBeInTheDocument()
    })
    expect(screen.getByText('Program Counter')).toBeInTheDocument()
  })

  it('advances program counter while running Add.hack', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Add.hack')

    fireEvent.click(screen.getByTitle('Run Simulation'))

    await waitFor(() => {
      expect(screen.getByText(/HARDWARE SIMULATOR \(PC: [1-9]\d*, Cycles: [1-9]\d*\)/)).toBeInTheDocument()
    }, { timeout: 2000 })
  })

  it('draws screen when simulation is running and screen memory has active bits', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    const [addressInput, valueInput] = screen.getAllByRole('spinbutton')

    fireEvent.change(addressInput, { target: { value: '16384' } })
    fireEvent.change(valueInput, { target: { value: '-32768' } })
    fireEvent.click(valueInput.parentElement.querySelector('button'))

    mockCanvasContext.fillRect.mockClear()

    fireEvent.click(screen.getByTitle('Run Simulation'))

    await waitFor(() => {
      expect(mockCanvasContext.fillRect).toHaveBeenCalledWith(0, 0, 1, 1)
    })
  })

  it('allows RAM edits while stopped', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    const inputs = screen.getAllByRole('spinbutton')
    const [addressInput, valueInput] = inputs

    fireEvent.change(addressInput, { target: { value: '10' } })
    fireEvent.change(valueInput, { target: { value: '123' } })
    const saveButton = valueInput.parentElement.querySelector('button')
    expect(saveButton).not.toBeNull()
    fireEvent.click(saveButton)

    expect(await screen.findByText(/Current value at 10:/)).toBeInTheDocument()
    expect(screen.getByText('123')).toBeInTheDocument()
  })

  it('stores RAM values as 16-bit numbers', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    const [addressInput, valueInput] = screen.getAllByRole('spinbutton')

    fireEvent.change(addressInput, { target: { value: '25' } })
    fireEvent.change(valueInput, { target: { value: '-1' } })
    fireEvent.click(valueInput.parentElement.querySelector('button'))

    expect(await screen.findByText(/Current value at 25:/)).toBeInTheDocument()
    expect(screen.getByText('65535')).toBeInTheDocument()
  })

  it('disables RAM editor while running', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    fireEvent.click(screen.getByTitle('Run Simulation'))

    const [addressInput, valueInput] = screen.getAllByRole('spinbutton')
    expect(addressInput).toBeDisabled()
    expect(valueInput).toBeDisabled()
  })

  it('captures keyboard input when PC keyboard is enabled and running', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    fireEvent.click(screen.getByTitle('Run Simulation'))

    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    expect(screen.getByRole('button', { name: 'ON' })).toBeInTheDocument()

    fireEvent.keyDown(window, { key: 'a' })

    expect(await screen.findByText('A')).toBeInTheDocument()
    expect(screen.getByText('Code: 65')).toBeInTheDocument()
  })

  it('captures SPACE and ENTER keyboard mappings when enabled', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    fireEvent.keyDown(window, { key: ' ' })
    expect(await screen.findByText('SPACE')).toBeInTheDocument()

    fireEvent.keyDown(window, { key: 'Enter' })
    expect(await screen.findByText('Key(128)')).toBeInTheDocument()
    expect(screen.getByText('Code: 128')).toBeInTheDocument()
  })

  it('resets current key shortly after keyup', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    fireEvent.keyDown(window, { key: 'a' })
    expect(await screen.findByText('Code: 65')).toBeInTheDocument()

    fireEvent.keyUp(window, { key: 'a' })
    await waitFor(() => {
      expect(screen.queryByText('Code: 65')).not.toBeInTheDocument()
    }, { timeout: 1000 })
  })

  it('maps keyboard input into RAM[24576] while enabled and running', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    await setRamValue(24576, 0)
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    fireEvent.keyDown(window, { key: 'a' })

    await waitFor(() => {
      expect(screen.getByText(/Current value at 24576:/).textContent).toContain('65')
    })

    fireEvent.keyUp(window, { key: 'a' })

    await waitFor(() => {
      expect(screen.getByText(/Current value at 24576:/).textContent).toContain('0')
    }, { timeout: 1000 })
  })

  it('ignores non-mapped special keys for keyboard display', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    fireEvent.keyDown(window, { key: 'ArrowLeft' })

    expect(screen.queryByText(/Code:/)).not.toBeInTheDocument()
    expect(screen.getByText('None')).toBeInTheDocument()
  })

  it('ignores keyboard events from focused input fields', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    const [addressInput] = screen.getAllByRole('spinbutton')
    fireEvent.keyDown(addressInput, { key: 'a' })

    expect(screen.queryByText('Code: 65')).not.toBeInTheDocument()
  })

  it('ignores keyboard input when keyboard toggle is OFF', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.keyDown(window, { key: 'a' })

    expect(screen.queryByText('Code: 65')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'OFF' })).toBeInTheDocument()
  })

  it('resets keyboard toggle to OFF when simulation stops', async () => {
    render(<HardwareSimulator />)

    await openHackFile()
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))
    expect(screen.getByRole('button', { name: 'ON' })).toBeInTheDocument()

    fireEvent.click(screen.getByTitle('Stop Simulation'))
    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'OFF' })).toBeInTheDocument()
    })
  })

  it('rejects unsupported file extensions when creating files', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'notes.txt')

    expect(screen.getByText('Error: Only .asm, .vm, .jack, and .hack files are allowed. You tried to create: .txt')).toBeInTheDocument()
    expect(screen.queryByText('notes.txt')).not.toBeInTheDocument()
  })

  it('rejects files without an extension', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'Program')

    expect(screen.getByText('Error: File must have an extension (.asm, .vm, .jack, or .hack)')).toBeInTheDocument()
    expect(screen.queryByText('Program')).not.toBeInTheDocument()
  })

  it('cancels creation when name is empty', async () => {
    render(<HardwareSimulator />)

    fireEvent.click(screen.getByTitle('New Folder'))
    const input = await screen.findByPlaceholderText('New folder name')
    fireEvent.change(input, { target: { value: '   ' } })
    fireEvent.click(input.parentElement.querySelector('button'))

    await waitFor(() => {
      expect(screen.queryByPlaceholderText('New folder name')).not.toBeInTheDocument()
    })
  })

  it('creates and opens a new .asm file', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'Program.asm')
    const programEntries = screen.getAllByText('Program.asm')
    expect(programEntries.length).toBeGreaterThan(0)
    fireEvent.click(programEntries[0])

    expect(screen.getByTitle('Compile → .hack')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('// Start coding in ASM...')).toBeInTheDocument()
  })

  it('does not duplicate tabs when reopening the same file', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Add.hack')
    await openHackFile('Add.hack')

    const tabs = screen.getAllByText('Add.hack')
    expect(tabs.length).toBe(2)
  })

  it('closes active tab and focuses another open tab', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    await openHackFile('Add.hack')

    const addTab = screen.getAllByText('Add.hack').find((node) =>
      node.closest('div')?.className.includes('border-r')
    )
    const closeButton = addTab?.parentElement?.querySelector('button')
    expect(closeButton).not.toBeNull()

    fireEvent.click(closeButton)

    expect(screen.getByTitle('Run Simulation')).toBeInTheDocument()
    const rectangleTabs = screen.getAllByText('Rectangle.hack')
    expect(rectangleTabs.length).toBeGreaterThan(0)
  })

  it('compiles .asm file and displays backend output', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockResolvedValue({
      json: async () => ({ success: true, hack_code: '1110001100001000' }),
    })

    render(<HardwareSimulator />)
    await createRootItem('file', 'Program.asm')
    fireEvent.click(screen.getByText('Program.asm'))

    fireEvent.change(screen.getByRole('textbox'), { target: { value: '@2\nD=A' } })
    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('1110001100001000')).toBeInTheDocument()
    expect(fetchSpy).toHaveBeenCalledTimes(1)

    const [, request] = fetchSpy.mock.calls[0]
    const formData = request.body
    expect(formData.get('language')).toBe('assembly')
    expect(formData.get('is_folder')).toBe('false')
    expect(formData.get('target')).toBe('.hack')
  })

  it('shows backend compilation errors from response payload', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      json: async () => ({ success: false, error: 'Assembler syntax error' }),
    })

    render(<HardwareSimulator />)
    await createRootItem('file', 'Program.asm')
    await openFileByName('Program.asm')
    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('Error: Assembler syntax error')).toBeInTheDocument()
  })

  it('shows network error when compilation request fails', async () => {
    vi.spyOn(global, 'fetch').mockRejectedValue(new Error('Network down'))

    render(<HardwareSimulator />)
    await createRootItem('file', 'Program.asm')
    fireEvent.click(screen.getByText('Program.asm'))

    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('Error: Unable to connect to backend server')).toBeInTheDocument()
  })

  it('prevents duplicate compile requests while loading', async () => {
    const deferred = createDeferred()
    const fetchSpy = vi.spyOn(global, 'fetch').mockReturnValue(deferred.promise)

    render(<HardwareSimulator />)
    await createRootItem('file', 'Program.asm')
    await openFileByName('Program.asm')

    const compileButton = screen.getByTitle('Compile → .hack')
    fireEvent.click(compileButton)
    fireEvent.click(compileButton)

    expect(fetchSpy).toHaveBeenCalledTimes(1)

    deferred.resolve({
      json: async () => ({ success: true, hack_code: 'ok' }),
    })
    await screen.findByText('ok')
  })

  it('updates compile target via dropdown for vm files', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'Program.vm')
    fireEvent.click(screen.getByText('Program.vm'))

    fireEvent.click(screen.getByTitle('Select target language'))
    fireEvent.click(screen.getByText('.asm'))

    expect(screen.getByTitle('Compile → .asm')).toBeInTheDocument()
  })

  it('shows all target options for root jack files and applies selected target', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'Main.jack')
    await openFileByName('Main.jack')

    fireEvent.click(screen.getByTitle('Select target language'))

    expect(screen.getByText('.vm')).toBeInTheDocument()
    expect(screen.getByText('.asm')).toBeInTheDocument()
    expect(screen.getByText('.hack')).toBeInTheDocument()

    fireEvent.click(screen.getByText('.vm'))

    expect(screen.queryByText('Target Language')).not.toBeInTheDocument()
    expect(screen.getByTitle('Compile → .vm')).toBeInTheDocument()
  })

  it('hides target dropdown for non-root files and hack files', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    expect(screen.queryByTitle('Select target language')).not.toBeInTheDocument()

    await createRootItem('folder', 'VMFiles')
    await createFileInFolder('VMFiles', 'Nested.vm')
    await openFileByName('Nested.vm')
    expect(screen.queryByTitle('Select target language')).not.toBeInTheDocument()
  })

  it('compiles root vm file with selected target and vm language', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockResolvedValue({
      json: async () => ({ success: true, asm_code: '// asm output' }),
    })

    render(<HardwareSimulator />)
    await createRootItem('file', 'Program.vm')
    await openFileByName('Program.vm')

    fireEvent.click(screen.getByTitle('Select target language'))
    fireEvent.click(screen.getByText('.asm'))
    fireEvent.click(screen.getByTitle('Compile → .asm'))

    expect(await screen.findByText('// asm output')).toBeInTheDocument()

    const [, request] = fetchSpy.mock.calls[0]
    const formData = request.body
    expect(formData.get('language')).toBe('vm')
    expect(formData.get('target')).toBe('.asm')
    expect(formData.get('is_folder')).toBe('false')
  })

  it('shows loading output and disables compile while request is pending', async () => {
    const deferred = createDeferred()
    vi.spyOn(global, 'fetch').mockReturnValue(deferred.promise)

    render(<HardwareSimulator />)
    await createRootItem('file', 'Program.asm')
    await openFileByName('Program.asm')

    const compileButton = screen.getByTitle('Compile → .hack')
    fireEvent.click(compileButton)

    expect(screen.getByText('Compiling...')).toBeInTheDocument()
    expect(compileButton).toBeDisabled()

    deferred.resolve({
      json: async () => ({ success: true, hack_code: 'done' }),
    })

    expect(await screen.findByText('done')).toBeInTheDocument()
  })

  it('blocks jack compilation when file is not inside a folder', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch')

    render(<HardwareSimulator />)
    await createRootItem('file', 'Main.jack')
    fireEvent.click(screen.getByText('Main.jack'))

    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('Error: .jack files can only be compiled when placed inside a folder.')).toBeInTheDocument()
    expect(fetchSpy).not.toHaveBeenCalled()
  })

  it('compiles jack files as folder payload when inside a folder', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockResolvedValue({
      json: async () => ({ success: true, hack_code: '1010' }),
    })

    render(<HardwareSimulator />)

    await createRootItem('folder', 'Game')
    await createFileInFolder('Game', 'Main.jack')
    await createFileInFolder('Game', 'Utils.jack')

    await openFileByName('Main.jack')
    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('1010')).toBeInTheDocument()

    const [, request] = fetchSpy.mock.calls[0]
    const formData = request.body
    const files = formData.getAll('files')
    expect(formData.get('language')).toBe('jack')
    expect(formData.get('is_folder')).toBe('true')
    expect(formData.get('folder_name')).toBe('Game')
    expect(files).toHaveLength(2)
    expect(files.map((file) => file.name).sort()).toEqual(['Main.jack', 'Utils.jack'])
  })

  it('blocks asm compilation for files inside folders', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch')

    render(<HardwareSimulator />)

    await createRootItem('folder', 'ASMFiles')
    await createFileInFolder('ASMFiles', 'Nested.asm')
    await openFileByName('Nested.asm')

    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('Error: .asm and .vm files must be compiled outside of folders.')).toBeInTheDocument()
    expect(fetchSpy).not.toHaveBeenCalled()
  })

  it('creates nested files and keeps folder tree accessible', async () => {
    render(<HardwareSimulator />)

    await createRootItem('folder', 'Programs')
    fireEvent.click(screen.getByText('Programs'))

    const folderNode = screen.getByText('Programs').closest('div')
    expect(folderNode).not.toBeNull()

    const folderContainer = folderNode.parentElement
    const newFileEntry = within(folderContainer).getByText('New File')
    fireEvent.click(newFileEntry)

    const nestedInput = await screen.findByPlaceholderText('New file name')
    fireEvent.change(nestedInput, { target: { value: 'Main.vm' } })
    fireEvent.click(nestedInput.parentElement.querySelector('button'))

    expect(await screen.findByText('Main.vm')).toBeInTheDocument()
    fireEvent.click(screen.getByText('Programs'))

    await waitFor(() => {
      expect(screen.queryByText('Main.vm')).not.toBeInTheDocument()
    })
  })

  it('supports creating a root file with Enter key', async () => {
    render(<HardwareSimulator />)

    fireEvent.click(screen.getByTitle('New File'))
    const input = await screen.findByPlaceholderText('New file name')
    fireEvent.change(input, { target: { value: 'Quick.asm' } })
    fireEvent.keyDown(input, { key: 'Enter' })

    expect(await screen.findByText('Quick.asm')).toBeInTheDocument()
    expect(screen.getByTitle('Compile → .hack')).toBeInTheDocument()
  })

  it('persists edited content when switching between open tabs', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'Program.asm')
    await openFileByName('Program.asm')

    fireEvent.change(screen.getByRole('textbox'), { target: { value: '@2\nD=A\n@3' } })

    fireEvent.click(screen.getAllByText('Add.hack')[0])

    const programTab = screen.getAllByText('Program.asm').find((node) =>
      node.closest('div')?.className.includes('border-r')
    )
    expect(programTab).toBeDefined()
    fireEvent.click(programTab)

    await waitFor(() => {
      expect(screen.getByRole('textbox')).toHaveValue('@2\nD=A\n@3')
    })
  })

  it('returns to empty editor state after closing the last open tab', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Add.hack')

    const addTab = screen.getAllByText('Add.hack').find((node) =>
      node.closest('div')?.className.includes('border-r')
    )
    const closeButton = addTab?.parentElement?.querySelector('button')
    expect(closeButton).not.toBeNull()

    fireEvent.click(closeButton)

    await waitFor(() => {
      expect(screen.getByText('Open a file from the explorer to start editing')).toBeInTheDocument()
    })
    expect(screen.getByText('OUTPUT')).toBeInTheDocument()
  })

  it('starts with run/compile button disabled when no file is active', () => {
    render(<HardwareSimulator />)

    const runButton = screen.getByTitle('Compile → .hack')
    expect(runButton).toBeDisabled()
  })

  it('shows keyboard helper message changes for OFF, ON+stopped, and ON+running states', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')

    expect(screen.getByText('Toggle ON to enable keyboard input')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))
    expect(screen.getByText('Start simulation to use keyboard')).toBeInTheDocument()

    fireEvent.click(screen.getByTitle('Run Simulation'))
    expect(await screen.findByText('Press any key on your keyboard')).toBeInTheDocument()
  })

  it('shows OFF in key display while keyboard is disabled during running simulation', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Add.hack')
    fireEvent.click(screen.getByTitle('Run Simulation'))

    await screen.findByText('Current Key:')
    expect(screen.getAllByText('OFF').length).toBeGreaterThan(0)
    expect(screen.queryByText(/Code:/)).not.toBeInTheDocument()
  })

  it('clears RUNNING badge and returns controls to stopped state when stopping', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    fireEvent.click(screen.getByTitle('Run Simulation'))
    expect(await screen.findByText('RUNNING')).toBeInTheDocument()

    fireEvent.click(screen.getByTitle('Stop Simulation'))

    await waitFor(() => {
      expect(screen.queryByText('RUNNING')).not.toBeInTheDocument()
    })
    expect(screen.getByTitle('Run Simulation')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'OFF' })).toBeInTheDocument()
  })

  it('blocks vm compilation for files inside folders', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch')

    render(<HardwareSimulator />)

    await createRootItem('folder', 'VMGroup')
    await createFileInFolder('VMGroup', 'Nested.vm')
    await openFileByName('Nested.vm')

    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('Error: .asm and .vm files must be compiled outside of folders.')).toBeInTheDocument()
    expect(fetchSpy).not.toHaveBeenCalled()
  })

  it('resizes output panel using divider drag for non-hack files', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'Resize.asm')
    await openFileByName('Resize.asm')

    const outputHeader = screen.getByText('OUTPUT')
    const outputPanel = outputHeader.closest('div')?.parentElement
    expect(outputPanel).not.toBeNull()
    expect(outputPanel.style.width).toBe('400px')

    const divider = document.querySelector('div.cursor-col-resize')
    expect(divider).not.toBeNull()

    fireEvent.mouseDown(divider)
    fireEvent.mouseMove(window, { clientX: 500 })
    fireEvent.mouseUp(window)

    expect(outputPanel.style.width).toBe(`${window.innerWidth - 500}px`)
  })

  it('auto-resizes for .hack files and restores draggable divider for non-hack files', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')

    const hackPanel = screen.getByText(/HARDWARE SIMULATOR/).closest('div')?.parentElement
    expect(hackPanel).not.toBeNull()
    expect(hackPanel.style.width).not.toBe('400px')
    expect(document.querySelector('div.cursor-col-resize')).toBeNull()

    await createRootItem('file', 'Switch.asm')
    await openFileByName('Switch.asm')

    const outputPanel = screen.getByText('OUTPUT').closest('div')?.parentElement
    expect(outputPanel).not.toBeNull()
    expect(outputPanel.style.width).toBe('400px')
    expect(document.querySelector('div.cursor-col-resize')).not.toBeNull()
  })

  it('maps digit keyboard input when keyboard capture is enabled', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    fireEvent.keyDown(window, { key: '5' })

    expect(await screen.findByText('5')).toBeInTheDocument()
    expect(screen.getByText('Code: 53')).toBeInTheDocument()
  })

  it('ignores keyboard events from editor textarea while keyboard capture is enabled', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    const editor = screen.getByRole('textbox')
    fireEvent.keyDown(editor, { key: 'a' })

    expect(screen.queryByText('Code: 65')).not.toBeInTheDocument()
  })

  it('keeps RAM address unchanged when out-of-range address is entered', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    const [addressInput] = screen.getAllByRole('spinbutton')

    fireEvent.change(addressInput, { target: { value: '123' } })
    await waitFor(() => {
      expect(screen.getByText(/Current value at 123:/)).toBeInTheDocument()
    })

    fireEvent.change(addressInput, { target: { value: '30000' } })

    expect(screen.getByText(/Current value at 123:/)).toBeInTheDocument()
  })

  it('keeps RAM value unchanged when out-of-range value is entered', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    const [addressInput, valueInput] = screen.getAllByRole('spinbutton')

    fireEvent.change(addressInput, { target: { value: '42' } })
    fireEvent.change(valueInput, { target: { value: '12' } })
    fireEvent.change(valueInput, { target: { value: '40000' } })
    fireEvent.click(valueInput.parentElement.querySelector('button'))

    await waitFor(() => {
      expect(screen.getByText(/Current value at 42:/).textContent).toContain('12')
    })
  })

  it('keeps current active tab when closing an inactive tab', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    await openHackFile('Add.hack')

    const rectangleTab = screen.getAllByText('Rectangle.hack').find((node) =>
      node.closest('div')?.className.includes('border-r')
    )
    const closeButton = rectangleTab?.parentElement?.querySelector('button')
    expect(closeButton).not.toBeNull()

    fireEvent.click(closeButton)

    await waitFor(() => {
      expect(screen.getByText(/HARDWARE SIMULATOR \(PC: [1-9]\d*|HARDWARE SIMULATOR \(PC: 0, Cycles: 0\)/)).toBeInTheDocument()
    })
    expect(screen.getAllByText('Add.hack').length).toBeGreaterThan(0)
  })

  it('uses backend message field when compilation fails without error field', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      json: async () => ({ success: false, message: 'Compiler pipeline failed' }),
    })

    render(<HardwareSimulator />)
    await createRootItem('file', 'Message.asm')
    await openFileByName('Message.asm')

    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('Error: Compiler pipeline failed')).toBeInTheDocument()
  })

  it('compiles root vm file to default .hack target', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockResolvedValue({
      json: async () => ({ success: true, hack_code: '1010101010101010' }),
    })

    render(<HardwareSimulator />)
    await createRootItem('file', 'Default.vm')
    await openFileByName('Default.vm')

    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('1010101010101010')).toBeInTheDocument()

    const [, request] = fetchSpy.mock.calls[0]
    const formData = request.body
    expect(formData.get('language')).toBe('vm')
    expect(formData.get('target')).toBe('.hack')
    expect(formData.get('is_folder')).toBe('false')
  })

  it('sends edited active file content in compile request payload', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockResolvedValue({
      json: async () => ({ success: true, hack_code: '0000' }),
    })

    render(<HardwareSimulator />)
    await createRootItem('file', 'Payload.asm')
    await openFileByName('Payload.asm')

    const updatedSource = '@21\nD=A\n@22\nD=D+A'
    fireEvent.change(screen.getByRole('textbox'), { target: { value: updatedSource } })
    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('0000')).toBeInTheDocument()

    const [, request] = fetchSpy.mock.calls[0]
    const file = request.body.get('file')
    expect(await file.text()).toBe(updatedSource)
  })

  it('does not resize output panel when drag goes out of allowed bounds', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'Bounds.asm')
    await openFileByName('Bounds.asm')

    const outputPanel = screen.getByText('OUTPUT').closest('div')?.parentElement
    expect(outputPanel).not.toBeNull()
    expect(outputPanel.style.width).toBe('400px')

    const divider = document.querySelector('div.cursor-col-resize')
    expect(divider).not.toBeNull()

    fireEvent.mouseDown(divider)
    fireEvent.mouseMove(window, { clientX: window.innerWidth - 120 })
    fireEvent.mouseMove(window, { clientX: 80 })
    fireEvent.mouseUp(window)

    expect(outputPanel.style.width).toBe('400px')
  })

  it('maps ENTER key into RAM[24576] while keyboard capture is enabled and running', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    await setRamValue(24576, 0)
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    fireEvent.keyDown(window, { key: 'Enter' })

    await waitFor(() => {
      expect(screen.getByText(/Current value at 24576:/).textContent).toContain('128')
    })

    fireEvent.keyUp(window, { key: 'Enter' })

    await waitFor(() => {
      expect(screen.getByText(/Current value at 24576:/).textContent).toContain('0')
    }, { timeout: 1000 })
  })

  it('ignores keyup events originating from input fields', async () => {
    render(<HardwareSimulator />)

    await openHackFile('Rectangle.hack')
    fireEvent.click(screen.getByTitle('Run Simulation'))
    fireEvent.click(screen.getByRole('button', { name: 'OFF' }))

    fireEvent.keyDown(window, { key: 'a' })
    expect(await screen.findByText('Code: 65')).toBeInTheDocument()

    const [addressInput] = screen.getAllByRole('spinbutton')
    fireEvent.keyUp(addressInput, { key: 'a' })

    await waitFor(() => {
      expect(screen.getByText('Code: 65')).toBeInTheDocument()
    }, { timeout: 300 })
  })

  it('shows only .hack target option for root asm files', async () => {
    render(<HardwareSimulator />)

    await createRootItem('file', 'OnlyHack.asm')
    await openFileByName('OnlyHack.asm')

    fireEvent.click(screen.getByTitle('Select target language'))

    expect(screen.getByText('.hack')).toBeInTheDocument()
    expect(screen.queryByText('.asm')).not.toBeInTheDocument()
    expect(screen.queryByText('.vm')).not.toBeInTheDocument()
  })

  it('shows generic success message when backend returns success without code payload', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      json: async () => ({ success: true }),
    })

    render(<HardwareSimulator />)
    await createRootItem('file', 'NoPayload.asm')
    await openFileByName('NoPayload.asm')

    fireEvent.click(screen.getByTitle('Compile → .hack'))

    expect(await screen.findByText('Compilation successful')).toBeInTheDocument()
  })

  it('updates nested tree nodes when editing a root file with folders present', async () => {
    render(<HardwareSimulator />)

    await createRootItem('folder', 'FolderA')
    await createRootItem('folder', 'FolderB')
    await createRootItem('file', 'Root.asm')
    await openFileByName('Root.asm')

    const edited = '@1\nD=A\n@2\nD=D+A'
    fireEvent.change(screen.getByRole('textbox'), { target: { value: edited } })

    fireEvent.click(screen.getAllByText('Add.hack')[0])
    const rootTab = screen.getAllByText('Root.asm').find((node) =>
      node.closest('div')?.className.includes('border-r')
    )
    expect(rootTab).toBeDefined()
    fireEvent.click(rootTab)

    await waitFor(() => {
      expect(screen.getByRole('textbox')).toHaveValue(edited)
    })
  })

  it('adds file into the selected folder when multiple folders exist at root', async () => {
    render(<HardwareSimulator />)

    await createRootItem('folder', 'Alpha')
    await createRootItem('folder', 'Beta')

    fireEvent.click(screen.getByText('Beta'))
    fireEvent.click(screen.getByText('New File'))

    const nestedInput = await screen.findByPlaceholderText('New file name')
    fireEvent.change(nestedInput, { target: { value: 'InsideBeta.vm' } })
    fireEvent.keyDown(nestedInput, { key: 'Enter' })

    expect(await screen.findByText('InsideBeta.vm')).toBeInTheDocument()

    fireEvent.click(screen.getByText('Alpha'))
    fireEvent.click(screen.getByText('Beta'))

    expect(screen.getByText('InsideBeta.vm')).toBeInTheDocument()
  })
})
