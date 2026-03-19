export const toSigned16 = (value) => (value << 16) >> 16

export const executeHackInstruction = ({ instruction, aRegister, dRegister, pc, memory }) => {
  if ((instruction & 0b1000000000000000) === 0) {
    const value = instruction & 0b0111111111111111
    return {
      aRegister: value,
      dRegister,
      pc: (pc + 1) % 32768,
      memory,
    }
  }

  const comp = (instruction >> 6) & 0b1111111
  const dest = (instruction >> 3) & 0b111
  const jump = instruction & 0b111

  const aValue = memory[aRegister] || 0
  const dValue = dRegister

  let aluResult = 0
  switch (comp) {
    case 0b0101010:
      aluResult = 0
      break
    case 0b0111111:
      aluResult = 1
      break
    case 0b0111010:
      aluResult = -1
      break
    case 0b0001100:
      aluResult = dValue
      break
    case 0b0110000:
      aluResult = aRegister
      break
    case 0b1110000:
      aluResult = aValue
      break
    case 0b0001101:
      aluResult = ~dValue
      break
    case 0b0110001:
      aluResult = ~aRegister
      break
    case 0b1110001:
      aluResult = ~aValue
      break
    case 0b0001111:
      aluResult = -dValue
      break
    case 0b0110011:
      aluResult = -aRegister
      break
    case 0b1110011:
      aluResult = -aValue
      break
    case 0b0011111:
      aluResult = dValue + 1
      break
    case 0b0110111:
      aluResult = aRegister + 1
      break
    case 0b1110111:
      aluResult = aValue + 1
      break
    case 0b0001110:
      aluResult = dValue - 1
      break
    case 0b0110010:
      aluResult = aRegister - 1
      break
    case 0b1110010:
      aluResult = aValue - 1
      break
    case 0b0000010:
      aluResult = dValue + aRegister
      break
    case 0b1000010:
      aluResult = dValue + aValue
      break
    case 0b0010011:
      aluResult = dValue - aRegister
      break
    case 0b1010011:
      aluResult = dValue - aValue
      break
    case 0b0000111:
      aluResult = aRegister - dValue
      break
    case 0b1000111:
      aluResult = aValue - dValue
      break
    case 0b0000000:
      aluResult = dValue & aRegister
      break
    case 0b1000000:
      aluResult = dValue & aValue
      break
    case 0b0010101:
      aluResult = dValue | aRegister
      break
    case 0b1010101:
      aluResult = dValue | aValue
      break
    default:
      aluResult = 0
  }

  const normalized = aluResult & 0b1111111111111111
  const signedAluResult = toSigned16(aluResult)

  const nextARegister = (dest & 0b100) ? normalized : aRegister
  const nextDRegister = (dest & 0b010) ? normalized : dRegister

  let nextMemory = memory
  if (dest & 0b001) {
    if (aRegister < 24577) {
      nextMemory = [...memory]
      nextMemory[aRegister] = normalized
    }
  }

  const isZero = signedAluResult === 0
  const isNeg = signedAluResult < 0
  const isPos = signedAluResult > 0

  let shouldJump = false
  switch (jump) {
    case 0b001:
      shouldJump = isPos
      break
    case 0b010:
      shouldJump = isZero
      break
    case 0b011:
      shouldJump = isPos || isZero
      break
    case 0b100:
      shouldJump = isNeg
      break
    case 0b101:
      shouldJump = !isZero
      break
    case 0b110:
      shouldJump = isNeg || isZero
      break
    case 0b111:
      shouldJump = true
      break
  }

  return {
    aRegister: nextARegister,
    dRegister: nextDRegister,
    pc: shouldJump ? aRegister : (pc + 1) % 32768,
    memory: nextMemory,
  }
}