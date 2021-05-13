
# based on JCivED PIC reading code


def decode(codedData):
    plainData = [codedData[0]]
    i = 1
    while i < len(codedData):
        if codedData[i]!=0x90: # 0x90 is RLE control code for repetition
            plainData.append(codedData[i])
        else: # 0x90 encountered
            # Need to check if next byte value is 0 or not:
            if codedData[i+1]==0x0: # Then 0x90 is actual byte, not control code
                plainData.append(codedData[i])
                i += 1
            else: # Ok, we have a RLE code, let's manage it
                repeatCount = codedData[i+1]
                i += 1
                val = plainData[-1]
                for _ in range(0, repeatCount-1): plainData.append(val)
        i += 1
    return plainData


def encode(plainData):
    plainDataLen = len(plainData)
    codedData = [0] * (2 * plainDataLen)
    codedData[0] = plainData[0]
    cnt = 1
    repeating = False
    repeatCount = 0

    for i in range(1, plainDataLen):
        if plainData[i]!=plainData[i-1] or repeatCount==254:
            if repeating:
                codedData[cnt]=0x90
                codedData[cnt+1]=repeatCount+1
                cnt+=2
            repeating = False
            repeatCount = 0
            codedData[cnt]=plainData[i]
            if codedData[cnt]==0x90: # Escape fake control code
                codedData[cnt+1] = 0x0
                cnt += 1
            cnt += 1
        else:
            if repeating or (i<plainDataLen-2 and plainData[i+1]==plainData[i] and plainData[i+2]==plainData[i]):
                repeating = True
                repeatCount += 1
            else:
                repeating = False
                repeatCount = 0
                codedData[cnt]=plainData[i]
                if codedData[cnt]==0x90: # Escape fake control code
                    codedData[cnt+1]=0x0
                    cnt += 1
                cnt += 1
    if repeating:
        codedData[cnt]=0x90
        codedData[cnt+1]=repeatCount+1
        cnt+=2
    return codedData[:cnt]

