
# Based on JCivED PIC reading code, fixed and optimized


class LZWDictionary:

    def __init__(self, dicIndexMaxBits):
        self.dicTable = []
        self.curPos = 0

        self.dicTableLen = (0x1 << dicIndexMaxBits)
        # to optimize both directions:
        self.dict = {}
        self.table = []

        for i in range(0, 256):
            self.dict[chr(i)] = i
            self.table.append([i])

        self.table.append([])# 256th item

        self.curPos = 0x0101 # 257... For some reason...

    def serialize_key(self, entry):
        return ''.join(map(chr, entry))

    def getIndexOfEntry(self, entry):
        entry_s = self.serialize_key(entry)
        return self.dict.get(entry_s, -1)
        
    def addEntry(self, entry):
        entry_s = self.serialize_key(entry)
        if self.curPos < self.dicTableLen:
            self.dict[entry_s] = self.curPos
            self.table.append(entry)
            self.curPos += 1
        return self.curPos - 1
        
    def getEntry(self, pos):
        if pos < self.curPos:
            return self.table[pos]
        return None
        
    def getCurPos(self):
        return self.curPos

    def getSize(self):
        return self.dicTableLen

    def isFull(self):
        return self.getCurPos() >= self.getSize()

    def getLastEntry(self):
        return self.getEntry(self.getCurPos()-1)

    def toString(self, fr, to):
        sb = ''

        for i in range(fr, to):#self.curPos):
            sb += "[" + str(i) + "] => " + str(self.getEntry(i)) + "\n"

        return sb

# ENCODING:


def encode(inputData, dicIndexMaxBits = 0x0B):
    plainData = inputData
    codedData = []

    i = 0
    plainDataLen = len(plainData)
    while i < plainDataLen:
        dic = LZWDictionary(dicIndexMaxBits)
        buff = []

        while i < plainDataLen:
        
            testChunk = list(buff)
            testChunk.append(plainData[i])
            if dic.getIndexOfEntry(testChunk) != -1:
                buff = testChunk
            else:
                codedData.append(dic.getIndexOfEntry(buff))
                if dic.isFull():
                    break
                dic.addEntry(testChunk)
                buff = [plainData[i]]
            i += 1

        if not dic.isFull():
            codedData.append(dic.getIndexOfEntry(buff))
            i += 1

    #print dic.toString(250, 260)
    return codedData;


def ints2bytes(lzwIndexes, mode):
    output = [] #[0]*(2*len(lzwIndexes.length)) # each input int will take *at most* 2 bytes, so initial size is a sufficient guess

    usableBits = 0
    usableBitCount = 0

    indicatorLength = 1 # /* to increment with ++; rule is that 8+indicatorLength must be <= ubyte_mode, otherwise reset */
    #//int indicatorFlag = 0x001; /* to increment with <<=1 followed by |= 1 */
    nextThreshold = 0x0100 #/*255*/; /* to increment with <<=1, or *=2 */
    codedCounter = 0
    dicCounter = 0

    remainingIndexesToCode = len(lzwIndexes)

    #//while(decodedCounter<256) {
    #//for(int i=0;i<imageData.length;i++) {
    while remainingIndexesToCode>0:
        #/* get enough coded bits to work with */
        while usableBitCount<8:
            #//usableBits|=(ledis.readUnsignedByte()<<usableBitCount);
            usableBits |= (lzwIndexes[codedCounter]<<usableBitCount)
            codedCounter += 1

            remainingIndexesToCode -= 1
            usableBitCount += (8+indicatorLength)

            dicCounter+=1
            if dicCounter==nextThreshold:
                dicCounter = 0
                indicatorLength+=1 #/* to increment with ++; rule is that 8+indicatorLength must be <= ubyte_mode, otherwise reset */
                #//indicatorFlag<<=1; indicatorFlag|=1;/* to increment with <<=1 followed by |= 1 */
                nextThreshold<<=1 #/* to increment with <<=1, or *=2 */

                if 8+indicatorLength>mode:
                    dicCounter = 0
                    indicatorLength = 1
                    #//indicatorFlag = 0x001; 
                    nextThreshold = 0x0100 #/*256*/;

        #/* decode bytes and indicators */
        while usableBitCount>=8:
            byteToWrite = usableBits & 0xFF
            output.append(byteToWrite)
            usableBits >>= 8
            usableBitCount -= 8

    # Write remnant bits
    if usableBitCount>0:
        byteToWrite = usableBits & 0xFF
        output.append(byteToWrite)
    #for x in range(0,26): output.append(0)
    return output;


def compress(data, mode=11):
    enc_data = encode(data)
    #print 'ENC', enc_data[500:800], len(enc_data)
    return ints2bytes(enc_data, mode)


# DECODING:


def decode(inputData, dicIndexMaxBits=0x0B):
    codedData = inputData
    plainData = []
    i = 0
    codedDataLength = len(codedData)

    while i < codedDataLength:
        dic = LZWDictionary(dicIndexMaxBits)
        w = [codedData[i]]
        plainData.append(codedData[i])

        while not dic.isFull() and i < codedDataLength-1:
            i += 1
            k = codedData[i]

            entry = []
            de = dic.getEntry(k)
            #print i, k, de, w
            if de is not None:
                entry = de
            elif k == dic.getCurPos():
                entry = w + [w[0]]
            else:
                print "No dictionary entry in LZW dict !!! (", i, k, de, w ,")"
                return plainData
            #print 'ent', entry

            # Append entry to the result stream (plainData) 
            plainData += entry
            # Add w+entry[0] to the dictionary.
            dic.addEntry(w + [entry[0]])

            w = entry
            #print dic.toString(250, 260)

        i += 1

        #/* First append plainData to decodedData */
        #int ddl = decodedData.length;
        #decodedData = Arrays.copyOf(decodedData, decodedData.length + plainDataLen);
        #for(int k=0; k<plainDataLen; k++) {
        #    decodedData[ddl+k] = plainData[k];
        #}
        #/* Second truncate codedData to keep only undecoded stuff before continuing the loop */
        #codedData = Arrays.copyOfRange(codedData, i+1, codedData.length);

    return plainData;



def bytes2ints(data, ubyte_mode):
        remainingCodedBytes = len(data)
        parsedIndexes = []

        usableBits = 0
        usableBitCount = 0

        indicatorLength = 1 # /* to increment with ++; rule is that 8+indicatorLength must be <= ubyte_mode, otherwise reset */
        indicatorFlag = 0x001 # /* to increment with <<=1 followed by |= 1 */
        nextThreshold = 0x0100 #/*256*/; /* to increment with <<=1, or *=2 */
        decodedCounter = 0

        #/** Legacy #1 */
        Index = 0
        #/** Legacy #1 end */

        while remainingCodedBytes > 0:
            #/* get enough coded bits to work with */
            while usableBitCount < 8+indicatorLength:
                usableBits|=(data.pop(0)<<usableBitCount)
                remainingCodedBytes-=1
                usableBitCount += 8

            #/* decode bytes and indicators */
            while usableBitCount>=8+indicatorLength:
                #/** Legacy #2
                # ** For us, Index = decodedIndicator<<8 | decodedByte; Or also: Index = usableBits & (indicatorFlag<<8 | 0xFF)
                # ** TempIndex = Index; fine... 
                # ** Testing legacy code 
                # */
                Index = usableBits & ( ( (indicatorFlag<<8) & 0xFF00) | 0x00FF )
                #/** Legacy #2 end */

                #//int decodedByte = usableBits & 0xFF;
                usableBits>>=8
                usableBitCount-=8

                #//int decodedIndicator = usableBits & indicatorFlag;
                usableBits>>=indicatorLength
                usableBitCount-=indicatorLength

                decodedCounter+=1

                if(decodedCounter==nextThreshold):
                    decodedCounter = 0
                    indicatorLength+=1 # /* to increment with ++; rule is that 8+indicatorLength must be <= ubyte_mode, otherwise reset */
                    indicatorFlag<<=1
                    indicatorFlag|=1 #/* to increment with <<=1 followed by |= 1 */
                    nextThreshold<<=1 # /* to increment with <<=1, or *=2 */

                    if 8+indicatorLength>ubyte_mode:
                        decodedCounter = 0
                        indicatorLength = 1
                        indicatorFlag = 0x001
                        nextThreshold = 0x0100 # /*256*/;

                parsedIndexes.append(Index)

        #/* Creating an int[] from Indexes */
        '''
        int[] intIndexes = new int[parsedIndexes.size()];
        for(int i=0; i<intIndexes.length; i++) {
            intIndexes[i] = parsedIndexes.get(i);
        }'''
        #print 'DEC', parsedIndexes[500:800], len(parsedIndexes)
        return parsedIndexes #intIndexes;


def decompress(data, mode=11):
    lzw_data = bytes2ints(data, mode)
    #print 'DEC', lzw_data[500:800], len(lzw_data)
    return decode(lzw_data)

