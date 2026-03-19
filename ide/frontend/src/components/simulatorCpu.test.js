import { describe, expect, it } from 'vitest'
import { executeHackInstruction, toSigned16 } from './simulatorCpu'

const makeCInstruction = ({ comp, dest = 0b000, jump = 0b000 }) => (
  0b1110000000000000 | (comp << 6) | (dest << 3) | jump
)

const createState = (overrides = {}) => ({
  aRegister: 0,
  dRegister: 0,
  pc: 0,
  memory: new Array(24577).fill(0),
  ...overrides,
})

describe('simulatorCpu', () => {
  it('converts numbers to signed 16-bit values', () => {
    expect(toSigned16(0x0000)).toBe(0)
    expect(toSigned16(0x7fff)).toBe(32767)
    expect(toSigned16(0x8000)).toBe(-32768)
    expect(toSigned16(0xffff)).toBe(-1)
  })

  it('executes A-instruction by loading A and incrementing PC', () => {
    const state = createState({ aRegister: 9, dRegister: 4, pc: 10 })
    const result = executeHackInstruction({
      ...state,
      instruction: 0b0000000000010101,
    })

    expect(result.aRegister).toBe(21)
    expect(result.dRegister).toBe(4)
    expect(result.pc).toBe(11)
    expect(result.memory).toBe(state.memory)
  })

  it('wraps program counter on A-instruction at 32767', () => {
    const state = createState({ pc: 32767 })
    const result = executeHackInstruction({ ...state, instruction: 0b0000000000000010 })

    expect(result.pc).toBe(0)
  })

  it('computes D+1 and stores to A and D when destination bits are set', () => {
    const state = createState({ aRegister: 10, dRegister: 5, pc: 8 })
    const instruction = makeCInstruction({ comp: 0b0011111, dest: 0b110 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.aRegister).toBe(6)
    expect(result.dRegister).toBe(6)
    expect(result.pc).toBe(9)
    expect(result.memory).toBe(state.memory)
  })

  it('uses M value for comp=M and writes result into D', () => {
    const memory = new Array(24577).fill(0)
    memory[12] = 345
    const state = createState({ aRegister: 12, dRegister: 7, memory })
    const instruction = makeCInstruction({ comp: 0b1110000, dest: 0b010 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.dRegister).toBe(345)
    expect(result.aRegister).toBe(12)
  })

  it('writes memory at current A when M destination bit is set', () => {
    const memory = new Array(24577).fill(0)
    const state = createState({ aRegister: 20, dRegister: 2, memory })
    const instruction = makeCInstruction({ comp: 0b0111010, dest: 0b001 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.memory).not.toBe(memory)
    expect(result.memory[20]).toBe(65535)
    expect(result.dRegister).toBe(2)
    expect(result.aRegister).toBe(20)
  })

  it('skips memory write when A is outside RAM bounds', () => {
    const memory = new Array(24577).fill(0)
    const state = createState({ aRegister: 30000, dRegister: 5, memory })
    const instruction = makeCInstruction({ comp: 0b0001100, dest: 0b001 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.memory).toBe(memory)
  })

  it('supports combined AMD destination with old A as memory index', () => {
    const memory = new Array(24577).fill(0)
    const state = createState({ aRegister: 30, dRegister: 0, memory })
    const instruction = makeCInstruction({ comp: 0b0111111, dest: 0b111 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.aRegister).toBe(1)
    expect(result.dRegister).toBe(1)
    expect(result.memory[30]).toBe(1)
  })

  it('defaults unknown comp codes to zero', () => {
    const state = createState({ aRegister: 4, dRegister: 9, pc: 2 })
    const instruction = makeCInstruction({ comp: 0b0100100, dest: 0b010 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.dRegister).toBe(0)
    expect(result.pc).toBe(3)
  })

  it.each([
    ['JGT true on positive result', 0b0111111, 0b001, 40, 40],
    ['JGT false on zero result', 0b0101010, 0b001, 40, 8],
    ['JEQ true on zero result', 0b0101010, 0b010, 12, 12],
    ['JGE true on zero result', 0b0101010, 0b011, 12, 12],
    ['JLT true on negative result', 0b0111010, 0b100, 18, 18],
    ['JNE true on negative result', 0b0111010, 0b101, 18, 18],
    ['JLE true on zero result', 0b0101010, 0b110, 22, 22],
    ['JMP always jumps', 0b0111111, 0b111, 77, 77],
  ])('%s', (_label, comp, jump, aRegister, expectedPc) => {
    const state = createState({ aRegister, pc: 7 })
    const instruction = makeCInstruction({ comp, jump })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.pc).toBe(expectedPc)
  })

  it('increments PC for C-instruction when jump condition is not met', () => {
    const state = createState({ aRegister: 99, pc: 55 })
    const instruction = makeCInstruction({ comp: 0b0111010, jump: 0b001 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.pc).toBe(56)
  })

  it('wraps program counter for C-instruction when not jumping at 32767', () => {
    const state = createState({ aRegister: 12, dRegister: 4, pc: 32767 })
    const instruction = makeCInstruction({ comp: 0b0001100 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.pc).toBe(0)
  })

  it.each([
    ['JGT false on negative result', 0b0111010, 0b001],
    ['JEQ false on positive result', 0b0111111, 0b010],
    ['JGE false on negative result', 0b0111010, 0b011],
    ['JLT false on zero result', 0b0101010, 0b100],
    ['JNE false on zero result', 0b0101010, 0b101],
    ['JLE false on positive result', 0b0111111, 0b110],
  ])('%s', (_label, comp, jump) => {
    const state = createState({ aRegister: 321, pc: 19 })
    const instruction = makeCInstruction({ comp, jump })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.pc).toBe(20)
  })

  it('updates only A register when destination is A', () => {
    const initialMemory = new Array(24577).fill(0)
    initialMemory[8] = 1234

    const state = createState({ aRegister: 8, dRegister: 31, memory: initialMemory })
    const instruction = makeCInstruction({ comp: 0b0011111, dest: 0b100 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.aRegister).toBe(32)
    expect(result.dRegister).toBe(31)
    expect(result.memory).toBe(initialMemory)
    expect(result.memory[8]).toBe(1234)
  })

  it('updates only D register when destination is D', () => {
    const state = createState({ aRegister: 14, dRegister: 2 })
    const instruction = makeCInstruction({ comp: 0b0110011, dest: 0b010 })
    const result = executeHackInstruction({ ...state, instruction })

    expect(result.aRegister).toBe(14)
    expect(result.dRegister).toBe(65522)
    expect(result.memory).toBe(state.memory)
  })

  it.each([
    ['0', 0b0101010, ({ dRegister, aRegister }) => 0],
    ['1', 0b0111111, ({ dRegister, aRegister }) => 1],
    ['-1', 0b0111010, ({ dRegister, aRegister }) => -1],
    ['D', 0b0001100, ({ dRegister, aRegister }) => dRegister],
    ['A', 0b0110000, ({ dRegister, aRegister }) => aRegister],
    ['!D', 0b0001101, ({ dRegister, aRegister }) => ~dRegister],
    ['!A', 0b0110001, ({ dRegister, aRegister }) => ~aRegister],
    ['-D', 0b0001111, ({ dRegister, aRegister }) => -dRegister],
    ['-A', 0b0110011, ({ dRegister, aRegister }) => -aRegister],
    ['D+1', 0b0011111, ({ dRegister, aRegister }) => dRegister + 1],
    ['A+1', 0b0110111, ({ dRegister, aRegister }) => aRegister + 1],
    ['D-1', 0b0001110, ({ dRegister, aRegister }) => dRegister - 1],
    ['A-1', 0b0110010, ({ dRegister, aRegister }) => aRegister - 1],
    ['D+A', 0b0000010, ({ dRegister, aRegister }) => dRegister + aRegister],
    ['D-A', 0b0010011, ({ dRegister, aRegister }) => dRegister - aRegister],
    ['A-D', 0b0000111, ({ dRegister, aRegister }) => aRegister - dRegister],
    ['D&A', 0b0000000, ({ dRegister, aRegister }) => dRegister & aRegister],
    ['D|A', 0b0010101, ({ dRegister, aRegister }) => dRegister | aRegister],
  ])('evaluates A-mode comp correctly for %s', (_label, comp, evaluateExpression) => {
    const state = createState({ aRegister: 5, dRegister: 3, pc: 100 })
    const instruction = makeCInstruction({ comp, dest: 0b010 })
    const result = executeHackInstruction({ ...state, instruction })

    const expectedValue = evaluateExpression({ dRegister: state.dRegister, aRegister: state.aRegister }) & 0xffff
    expect(result.dRegister).toBe(expectedValue)
    expect(result.aRegister).toBe(5)
    expect(result.memory).toBe(state.memory)
    expect(result.pc).toBe(101)
  })

  it.each([
    ['M', 0b1110000, ({ dRegister, memoryValue }) => memoryValue],
    ['!M', 0b1110001, ({ dRegister, memoryValue }) => ~memoryValue],
    ['-M', 0b1110011, ({ dRegister, memoryValue }) => -memoryValue],
    ['M+1', 0b1110111, ({ dRegister, memoryValue }) => memoryValue + 1],
    ['M-1', 0b1110010, ({ dRegister, memoryValue }) => memoryValue - 1],
    ['D+M', 0b1000010, ({ dRegister, memoryValue }) => dRegister + memoryValue],
    ['D-M', 0b1010011, ({ dRegister, memoryValue }) => dRegister - memoryValue],
    ['M-D', 0b1000111, ({ dRegister, memoryValue }) => memoryValue - dRegister],
    ['D&M', 0b1000000, ({ dRegister, memoryValue }) => dRegister & memoryValue],
    ['D|M', 0b1010101, ({ dRegister, memoryValue }) => dRegister | memoryValue],
  ])('evaluates M-mode comp correctly for %s', (_label, comp, evaluateExpression) => {
    const memory = new Array(24577).fill(0)
    memory[12] = 9

    const state = createState({ aRegister: 12, dRegister: 6, pc: 44, memory })
    const instruction = makeCInstruction({ comp, dest: 0b010 })
    const result = executeHackInstruction({ ...state, instruction })

    const expectedValue = evaluateExpression({ dRegister: state.dRegister, memoryValue: 9 }) & 0xffff
    expect(result.dRegister).toBe(expectedValue)
    expect(result.aRegister).toBe(12)
    expect(result.memory).toBe(memory)
    expect(result.pc).toBe(45)
  })
})