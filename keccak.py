# --------- Keccak (SHA-3) hashing algorithm ------------

def ROL64(a, n):
    return ((a >> (64-(n%64))) + (a << (n%64))) % (1 << 64)

def KeccakF1600onLanes(lanes):
    R = 1
    for round in range(24):
        # θ
        C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(5)]
        D = [C[(x+4)%5] ^ ROL64(C[(x+1)%5], 1) for x in range(5)]
        lanes = [[lanes[x][y]^D[x] for y in range(5)] for x in range(5)]
        # ρ and π
        (x, y) = (1, 0)
        current = lanes[x][y]
        for t in range(24):
            (x, y) = (y, (2*x+3*y)%5)
            (current, lanes[x][y]) = (lanes[x][y], ROL64(current, (t+1)*(t+2)//2))
        # χ
        for y in range(5):
            T = [lanes[x][y] for x in range(5)]
            for x in range(5):
                lanes[x][y] = T[x] ^((~T[(x+1)%5]) & T[(x+2)%5])
        # ι
        for j in range(7):
            R = ((R << 1) ^ ((R >> 7)*0x71)) % 256
            if (R & 2):
                lanes[0][0] = lanes[0][0] ^ (1 << ((1<<j)-1))
    return lanes

def load64(b):
    return sum((b[i] << (8*i)) for i in range(8))

def store64(a):
    return list((a >> (8*i)) % 256 for i in range(8))

def KeccakF1600(state):
    lanes = [[load64(state[8*(x+5*y):8*(x+5*y)+8]) for y in range(5)] for x in range(5)]
    lanes = KeccakF1600onLanes(lanes)
    state = bytearray(200)
    for x in range(5):
        for y in range(5):
            state[8*(x+5*y):8*(x+5*y)+8] = store64(lanes[x][y])
    return state

def Keccak(r, c, i, d, o):
    # where r - rate, c - capacity, i - inputBytes,  d - delimitedSuffix, o - outputByteLen

    # Initialization
    outputBytes = bytearray()
    state = bytearray([0 for i in range(200)])
    rateInBytes = r//8
    blockSize = 0
    if (((r + c) != 1600) or ((r % 8) != 0)):
        return
    inputOffset = 0

    # Absorb phase - absorbing all blocks from input bytes 
    while(inputOffset < len(i)):
        blockSize = min(len(i)-inputOffset, rateInBytes)
        for i in range(blockSize):
            state[i] = state[i] ^ i[i+inputOffset]
        inputOffset = inputOffset + blockSize
        if (blockSize == rateInBytes):
            state = KeccakF1600(state)
            blockSize = 0

    # Do the padding and processing to the squeezing phase
    state[blockSize] = state[blockSize] ^ d
    if (((d & 0x80) != 0) and (blockSize == (rateInBytes-1))):
        state = KeccakF1600(state)
    state[rateInBytes-1] = state[rateInBytes-1] ^ 0x80
    state = KeccakF1600(state)
    
    # Squeeze phase - squeezing out all blocks from the output bytes
    while(o > 0):
        blockSize = min(o, rateInBytes)
        outputBytes = outputBytes + state[0:blockSize]
        o = o - blockSize
        if (o > 0):
            state = KeccakF1600(state)
    return outputBytes

f = open('./bob_message.txt', 'rb')
b = bytearray(f.read())
print(Keccak(1088, 512, b, 0x06, 256//8))