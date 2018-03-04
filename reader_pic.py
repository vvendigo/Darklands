import sys
import os
from utils import bread, sread
import pygame


# Entirely based on Joel "Quadko" McIntyre PIC reading code


defaultPal = [ (0,0,0), (0,0,127), (0,127,0), (0,127,127), (127,0,0), (127,0,127), (127,127,0), (192,192,192), (127,127,127), (0,0,255), (0,255,0), (0,255,255), (255,0,0), (255,0,255), (255,255,0), (255,255,255), (0,0,0), (20,20,20), (32,32,32), (44,44,44), (56,56,56), (68,68,68), (80,80,80), (96,96,96), (112,112,112), (128,128,128), (144,144,144), (160,160,160), (180,180,180), (200,200,200), (224,224,224), (252,252,252), (0,0,252), (64,0,252), (124,0,252), (188,0,252), (252,0,252), (252,0,188), (252,0,124), (252,0,64), (252,0,0), (252,64,0), (252,124,0), (252,188,0), (252,252,0), (188,252,0), (124,252,0), (64,252,0), (0,252,0), (0,252,64), (0,252,124), (0,252,188), (0,252,252), (0,188,252), (0,124,252), (0,64,252), (124,124,252), (156,124,252), (188,124,252), (220,124,252), (252,124,252), (252,124,220), (252,124,188), (252,124,156), (252,124,124), (252,156,124), (252,188,124), (252,220,124), (252,252,124), (220,252,124), (188,252,124), (156,252,124), (124,252,124), (124,252,156), (124,252,188), (124,252,220), (124,252,252), (124,220,252), (124,188,252), (124,156,252), (180,180,252), (196,180,252), (216,180,252), (232,180,252), (252,180,252), (252,180,232), (252,180,216), (252,180,196), (252,180,180), (252,196,180), (252,216,180), (252,232,180), (252,252,180), (232,252,180), (216,252,180), (196,252,180), (180,252,180), (180,252,196), (180,252,216), (180,252,232), (180,252,252), (180,232,252), (180,216,252), (180,196,252), (0,0,112), (28,0,112), (56,0,112), (84,0,112), (112,0,112), (112,0,84), (112,0,56), (112,0,28), (112,0,0), (112,28,0), (112,56,0), (112,84,0), (112,112,0), (84,112,0), (56,112,0), (28,112,0), (0,112,0), (0,112,28), (0,112,56), (0,112,84), (0,112,112), (0,84,112), (0,56,112), (0,28,112), (56,56,112), (68,56,112), (84,56,112), (96,56,112), (112,56,112), (112,56,96), (112,56,84), (112,56,68), (112,56,56), (112,68,56), (112,84,56), (112,96,56), (112,112,56), (96,112,56), (84,112,56), (68,112,56), (56,112,56), (56,112,68), (56,112,84), (56,112,96), (56,112,112), (56,96,112), (56,84,112), (56,68,112), (80,80,112), (88,80,112), (96,80,112), (104,80,112), (112,80,112), (112,80,104), (112,80,96), (112,80,88), (112,80,80), (112,88,80), (112,96,80), (112,104,80), (112,112,80), (104,112,80), (96,112,80), (88,112,80), (80,112,80), (80,112,88), (80,112,96), (80,112,104), (80,112,112), (80,104,112), (80,96,112), (80,88,112), (0,0,64), (16,0,64), (32,0,64), (48,0,64), (64,0,64), (64,0,48), (64,0,32), (64,0,16), (64,0,0), (64,16,0), (64,32,0), (64,48,0), (64,64,0), (48,64,0), (32,64,0), (16,64,0), (0,64,0), (0,64,16), (0,64,32), (0,64,48), (0,64,64), (0,48,64), (0,32,64), (0,16,64), (32,32,64), (40,32,64), (48,32,64), (56,32,64), (64,32,64), (64,32,56), (64,32,48), (64,32,40), (64,32,32), (64,40,32), (64,48,32), (64,56,32), (64,64,32), (56,64,32), (48,64,32), (40,64,32), (32,64,32), (32,64,40), (32,64,48), (32,64,56), (32,64,64), (32,56,64), (32,48,64), (32,40,64), (44,44,64), (48,44,64), (52,44,64), (60,44,64), (64,44,64), (64,44,60), (64,44,52), (64,44,48), (64,44,44), (64,48,44), (64,52,44), (64,60,44), (64,64,44), (60,64,44), (52,64,44), (48,64,44), (44,64,44), (44,64,48), (44,64,52), (44,64,60), (44,64,64), (44,60,64), (44,52,64), (44,48,64), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0) ]


def readPal(data):
    pStart = data[0]
    pEnd = data[1]
    pos = 2
    pLen = pEnd - pStart
    out = [None]*256
    for i in xrange(0, pLen):
        out[pStart+i] = (data[pos]*4, data[pos+1]*4, data[pos+2]*4)
        pos += 3
    #print 'Pal', pStart, pEnd, pLen
    return out

class DecState:

    def __init__(self):
        self.StackTop = 0
        self.CurWordValue = 0
        self.Stack = [0]*500
        self.Data = None
        self.DataBitCount = 8
        self.PrevIndex = 0
        self.PrevPixel = 0
        self.CurIndex = 0
        self.FormatFlag = 0
        self.resetTable()

    def resetTable(self):
        self.BitMaskCount=9 # Max valid bit position
        self.BitMask=0x1ff # Max valid BitMasks
        # DecodeTable base index
        self.DecodeTableIndex=0x100; # why 100, top bit in BitMask? - Coincedence, plan?
        self.DecodeTable = [None]*0x800
        # Initial DecodeTable setting: Next=end of list, PixelData count from 0..0xff over and over
        for cnt in xrange(0, 0x800):
            self.DecodeTable[cnt] = (0xffff, cnt&0xff) # next, pixelData
#endclass

# turn file bits into pixel bits
def GetNextPixel(state):

    TempIndex = 0
    Index = 0
    CurBits = 0

    # if pixel stack is empty fill with decoded data from file
    if (state.StackTop==0):
        # Decode data from file buffer

        # Get current bits (?) from previous CurWordValue 
        # (which will have some already decode bits, some undecoded bits)
        # Discard known used bits, prep CurBits for more
        CurBits = state.CurWordValue>>(16-state.DataBitCount)

        # Get enough more bits from file data to be certain we have 
        # 1 full decodable bitstring
        while (state.DataBitCount < state.BitMaskCount):
            state.CurWordValue = bread(state.Data[state.CurIndex:state.CurIndex+2]) # Get next word (Image data:next word)
            state.CurIndex += 2
            CurBits |= (state.CurWordValue<<state.DataBitCount)&0xffff
            state.DataBitCount += 0x10

        # Update Databit count
        state.DataBitCount = state.DataBitCount-state.BitMaskCount

        # Get default Decode Lookup Index guesses
        Index=CurBits & state.BitMask
        TempIndex=Index

        # If default guess is invalid (or complex?) Set values to root lookup Index
        if (Index>=state.DecodeTableIndex):
            TempIndex = state.DecodeTableIndex
            Index = state.PrevIndex
            state.Stack[state.StackTop] = state.PrevPixel
            state.StackTop += 1

        # Folow DecodeTable list, adding each item's pixel to the stack until 
        # the end of the list (0xFFFF)
        while (state.DecodeTable[Index][0] != 0xFFFF):
            state.Stack[state.StackTop]=(Index&0xff00)+state.DecodeTable[Index][1] #PixelData
            state.StackTop += 1
            Index = state.DecodeTable[Index][0]# next

        # Push last node's pixel data, and remember pixel in 'PrevPixel'
        state.PrevPixel = state.DecodeTable[Index][1] #PixelData
        state.Stack[state.StackTop]=state.PrevPixel
        state.StackTop += 1

        # Set Decode Table data at this position
        state.DecodeTable[state.DecodeTableIndex] = (state.PrevIndex, state.PrevPixel)

        state.PrevIndex = TempIndex

        # Move to next 'initial' index and Update Bitflags if necessary
        state.DecodeTableIndex += 1
        if (state.DecodeTableIndex > state.BitMask):
            state.BitMaskCount += 1
            state.BitMask<<=1
            state.BitMask|=1

        # Reset Decode Table (and drop recorded pixel lists) if previous data grows too large
        if (state.BitMaskCount > state.FormatFlag):
            state.resetTable() #SetupDecodeTable(DecodeTable,BitMask,DecodeTableIndex,BitMaskCount);

    # Return pixel data from top of stack
    state.StackTop -= 1
    return state.Stack[state.StackTop] & 0xff


def readPic(data):
    state = DecState()

    CurIndex = 0
    Width = bread(data[CurIndex:CurIndex+2]) # Get next word (Width)
    CurIndex += 2
    Height = bread(data[CurIndex:CurIndex+2]) # Get next word (Height)
    CurIndex += 2

    CurWordValue=bread(data[CurIndex:CurIndex+2]) # Get next word (Image data:first word)
    CurIndex += 2
    FormatFlag = CurWordValue&0xff # First byte of Cur word

    if (FormatFlag>0xb): # Command is > 0xb Fix it
        CurWordValue=(CurWordValue&0xff00)+0xb
        FormatFlag=0xb

    RepeatCount = 0 # Pixel Repeat count=0
    CurPixelValue = 0 # Cur Pixel value; none at first!

    state.CurIndex = CurIndex
    state.Data = data
    state.CurWordValue = CurWordValue
    state.FormatFlag = FormatFlag

    picData = []

    for CurY in xrange(0, Height):
        picData.append([0]*Width)
        # Parse Data into line, a pixel at a time
        for CurX in xrange(0, Width):
            if (RepeatCount>0):# "RLE" Repeat count
                RepeatCount -= 1
            else:
                TempPixelValue = GetNextPixel(state)

                # If next value is not 'repeat last pixel flag' it is a new pixel
                if (TempPixelValue!=0x90):
                    CurPixelValue = TempPixelValue # Set Pixel Value
                # else get the value following the repeat flag (repeat count)
                else:
                    TempPixelValue = GetNextPixel(state)

                    # If the repeat count is 0, the 90 is a pixel value, not a rep instrution!
                    if (TempPixelValue==0):
                        CurPixelValue = 0x90
                    # Otherwise, setup the repeat
                    else:
                        # Already done pixel 1 (before 90), 
                        # will do pixel 2 right now, so adjust count 
                        # to correct 'future repeat' values
                        RepeatCount = TempPixelValue - 2

            # Just put the pixel in the bitmap for now
            #!!! ImageData[CurY*Width+CurX]=(unsigned char)CurPixelValue;
            #print CurPixelValue
            picData[CurY][CurX] = CurPixelValue

    return picData


def readFile(fname, palOnly = False):
    pal = None
    pic = None

    data = [ord(c) for c in open(fname).read()]
    dataLen = len(data)
    #print fname, dataLen
    pos = 0
    while pos < dataLen:
        tag = bread(data[pos:pos+2])
        pos += 2
        segLen = bread(data[pos:pos+2])
        pos += 2
        #print hex(tag), segLen
        if tag == 0x304D:
            pal = readPal(data[pos:pos+segLen])
            if palOnly:
                break
        elif tag == 0x3058 and not palOnly:
            pic = readPic(data[pos:pos+segLen])
        else: print 'Unknown!'
        pos += segLen
    return pal, pic


def renderImage(pal, pic):
    s = pygame.Surface((len(pic[0]), len(pic)), pygame.SRCALPHA, 32)
    #s = s.convert_alpha()
    for y, ln in enumerate(pic):
        for x, ci in enumerate(ln):
            c = pal[ci]
            if ci > 0 and c != None:
                s.fill(c, (x,y, 1, 1))
    return s


def getImage(fname, palExt = None):
    pal, pic = readFile(fname)
    if palExt: pal = palExt
    return renderImage(pal, pic)


def convertImage(infname, outfname, palExt = None):
    img = getImage(infname, palExt = None)
    pygame.image.save(img, outfname)


# main ------------
if __name__ == '__main__':
    fname = sys.argv[1]
    ddir = sys.argv[2]
    # opt. file to pallete read from
    pname = None
    if len(sys.argv) == 4:
        pname = sys.argv[3]

    dname = ddir + '/' + os.path.basename(fname) + '.png'
    pal, pic = readFile(fname)

    print fname,
    if pic:
        print 'pic', len(pic[0]), len(pic),
    #print pic[0][0]
    if pal:
        print 'pal', len(pal), pal
    print

    if pname:
        pal, _ = readFile(pname, palOnly=True)

    if not pal:
        pal = defaultPal
    
    if pic:
        img = renderImage(pal, pic)
        pygame.image.save(img, dname)
    else:
        print '!!!'

