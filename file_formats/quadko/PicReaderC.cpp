#include "stdafx.h"
#include "PicReaderC.h"

CPicReaderC::CPicReaderC()
{
	Valid=false;
	Width=0;
	Height=0;

	FileData=NULL;
	FileDataLen=0;
	CurFileOffset=0;

	PaletteExists=false;

	ImageData=NULL;
	ImageDataLen=NULL;

	InitPalette();
}

CPicReaderC::~CPicReaderC()
{

}

bool CPicReaderC::Load(const char *Filename)
{
	bool RetVal=false;

	HANDLE File;
	File=CreateFile(Filename,GENERIC_READ,FILE_SHARE_READ,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL);

	if (File!=NULL)
	{
		if (FileData!=NULL)
		{
			delete [] FileData;
			FileData=NULL;
		}

		FileDataLen=GetFileSize(File,NULL);

		if (FileDataLen==-1)
		{
			FileDataLen=SetFilePointer(File,0,NULL,FILE_END);
			SetFilePointer(File,0,NULL,FILE_BEGIN);
		}

		FileData=new unsigned char[FileDataLen];

		ReadFile(File,FileData,FileDataLen,(unsigned long*)&FileDataLen,NULL);

		if (FileDataLen==0)
		{
			delete [] FileData;
			FileData=NULL;
		}
		// Data In Buffer
		else
		{
			RetVal=Load(FileData,FileDataLen);
		}

		CloseHandle(File);
	}
	return RetVal;
}

// Load a file from memory buf into meaningful parts
bool CPicReaderC::Load(void *Buf, int BufLen)
{
	bool RetVal=false;
	int MaxOffset;
	unsigned short Tag;
	int Len;

	// Setup Memory
	if (Buf!=(void*)FileData)
	{
		if (FileData!=NULL)
		{
			delete [] FileData;
			FileData=NULL;
			FileDataLen=0;
		}

		FileDataLen=BufLen;
		FileData = new unsigned char [FileDataLen];
		CopyMemory(FileData,Buf,FileDataLen);
	}

	RetVal=true;

	if (RetVal)
	{
		MaxOffset=FileDataLen;
		CurFileOffset=0;

		while (CurFileOffset<MaxOffset)
		{
			Tag=0;
			Len=0;

			//FileData.Read(&Tag,2);
			//FileData.Read(&Len,2);

			CopyMemory(&Tag,FileData+CurFileOffset,2);
			CurFileOffset+=2;
			CopyMemory(&Len,FileData+CurFileOffset,2);
			CurFileOffset+=2;

			switch (Tag)
			{
				case 0x304D: //M0- Palette Data
				{
					SetPaletteM0(FileData+CurFileOffset,Len);
					CurFileOffset+=Len;
					
				}
				break;
				case 0x3058: //X0- Image Data
				{
					SetImageX0(FileData+CurFileOffset,Len);
					CurFileOffset+=Len;
					Valid=true;
				}
				break;
				default:
				{
					// Error
					//"You have found an unknown InternalData format!";
					CurFileOffset=MaxOffset;
				}
				break;
			};
		}

		// Done with file data
		if (FileData!=NULL)
		{
			delete [] FileData;
			FileData=NULL;
			FileDataLen=0;
		}
	}

	return RetVal;
}

// Single Pixel Funcs
COLORREF CPicReaderC::GetPixel(int X, int Y)
{
	COLORREF RetVal=RGB(0,0,0);

	if (Valid && X<Width && Y<Height)
	{
		RetVal=GetColor(ImageData[Y*Width+X]);		
	}

	return RetVal;
}

unsigned char CPicReaderC::GetPixelByte(int X, int Y)
{
	unsigned char RetVal=0;

	if (Valid && X<Width && Y<Width)
	{
		RetVal=ImageData[Y*Width+X];
	}

	return RetVal;
}

// Full Pixel Buffer funcs
int CPicReaderC::GetPixelData(char *Buf, int BufLen)
{
	int RetVal=0;

	if (Valid)
	{
		RetVal=Width*Height*3; // * 3 rgb bytes per pixel
		BufLen=min(BufLen,RetVal);
		
		TByteRGBC *RGBBuf=(TByteRGBC *)Buf;

		int Index,Max;

		Index=0;
		Max=BufLen/3;

		while (Index<Max)
		{
			CopyMemory(&RGBBuf[Index],&Palette[ImageData[Index]],3);
			Index++;
		}
	}

	return RetVal;
}

int CPicReaderC::GetPixelByteData(char *Buf, int BufLen)
{
	int RetVal=0;

	if (Valid)
	{
		RetVal=Width*Height;
		CopyMemory(Buf,ImageData,min(BufLen,RetVal));
	}

	return RetVal;
}

// Color Funcs
COLORREF CPicReaderC::GetColor(unsigned int Index)
{
	COLORREF RetVal=RGB(0,0,0);

	if (Index<256)
	{
		RetVal=Palette[Index];
	}

	return RetVal;
}

void CPicReaderC::SetColor(unsigned int Index, COLORREF NewColor)
{
	if (Index<256)
	{
		Palette[Index]=NewColor;
	}
}


void CPicReaderC::InitPalette()
{
	// Start out with the standard VGA Palette; it's not right, but is something
	Palette[  0]=RGB(0,0,0);
	Palette[  1]=RGB(0,0,127);
	Palette[  2]=RGB(0,127,0);
	Palette[  3]=RGB(0,127,127);
	Palette[  4]=RGB(127,0,0);
	Palette[  5]=RGB(127,0,127);
	Palette[  6]=RGB(127,127,0);
	Palette[  7]=RGB(192,192,192);
	Palette[  8]=RGB(127,127,127);
	Palette[  9]=RGB(0,0,255);
	Palette[ 10]=RGB(0,255,0);
	Palette[ 11]=RGB(0,255,255);
	Palette[ 12]=RGB(255,0,0);
	Palette[ 13]=RGB(255,0,255);
	Palette[ 14]=RGB(255,255,0);
	Palette[ 15]=RGB(255,255,255); // end primary 16
	Palette[ 16]=RGB(0,0,0);
	Palette[ 17]=RGB(20,20,20);
	Palette[ 18]=RGB(32,32,32);
	Palette[ 19]=RGB(44,44,44);
	Palette[ 20]=RGB(56,56,56);
	Palette[ 21]=RGB(68,68,68);
	Palette[ 22]=RGB(80,80,80);
	Palette[ 23]=RGB(96,96,96);
	Palette[ 24]=RGB(112,112,112);
	Palette[ 25]=RGB(128,128,128);
	Palette[ 26]=RGB(144,144,144);
	Palette[ 27]=RGB(160,160,160);
	Palette[ 28]=RGB(180,180,180);
	Palette[ 29]=RGB(200,200,200);
	Palette[ 30]=RGB(224,224,224);
	Palette[ 31]=RGB(252,252,252); // end greyscale
	Palette[ 32]=RGB(0,0,252);
	Palette[ 33]=RGB(64,0,252);
	Palette[ 34]=RGB(124,0,252);
	Palette[ 35]=RGB(188,0,252);
	Palette[ 36]=RGB(252,0,252);
	Palette[ 37]=RGB(252,0,188);
	Palette[ 38]=RGB(252,0,124);
	Palette[ 39]=RGB(252,0,64);
	Palette[ 40]=RGB(252,0,0);
	Palette[ 41]=RGB(252,64,0);
	Palette[ 42]=RGB(252,124,0);
	Palette[ 43]=RGB(252,188,0);
	Palette[ 44]=RGB(252,252,0);
	Palette[ 45]=RGB(188,252,0);
	Palette[ 46]=RGB(124,252,0);
	Palette[ 47]=RGB(64,252,0);
	Palette[ 48]=RGB(0,252,0);
	Palette[ 49]=RGB(0,252,64);
	Palette[ 50]=RGB(0,252,124);
	Palette[ 51]=RGB(0,252,188);
	Palette[ 52]=RGB(0,252,252);
	Palette[ 53]=RGB(0,188,252);
	Palette[ 54]=RGB(0,124,252);
	Palette[ 55]=RGB(0,64,252);
	Palette[ 56]=RGB(124,124,252);
	Palette[ 57]=RGB(156,124,252);
	Palette[ 58]=RGB(188,124,252);
	Palette[ 59]=RGB(220,124,252);
	Palette[ 60]=RGB(252,124,252);
	Palette[ 61]=RGB(252,124,220);
	Palette[ 62]=RGB(252,124,188);
	Palette[ 63]=RGB(252,124,156);
	Palette[ 64]=RGB(252,124,124);
	Palette[ 65]=RGB(252,156,124);
	Palette[ 66]=RGB(252,188,124);
	Palette[ 67]=RGB(252,220,124);
	Palette[ 68]=RGB(252,252,124);
	Palette[ 69]=RGB(220,252,124);
	Palette[ 70]=RGB(188,252,124);
	Palette[ 71]=RGB(156,252,124);
	Palette[ 72]=RGB(124,252,124);
	Palette[ 73]=RGB(124,252,156);
	Palette[ 74]=RGB(124,252,188);
	Palette[ 75]=RGB(124,252,220);
	Palette[ 76]=RGB(124,252,252);
	Palette[ 77]=RGB(124,220,252);
	Palette[ 78]=RGB(124,188,252);
	Palette[ 79]=RGB(124,156,252);
	Palette[ 80]=RGB(180,180,252);
	Palette[ 81]=RGB(196,180,252);
	Palette[ 82]=RGB(216,180,252);
	Palette[ 83]=RGB(232,180,252);
	Palette[ 84]=RGB(252,180,252);
	Palette[ 85]=RGB(252,180,232);
	Palette[ 86]=RGB(252,180,216);
	Palette[ 87]=RGB(252,180,196);
	Palette[ 88]=RGB(252,180,180);
	Palette[ 89]=RGB(252,196,180);
	Palette[ 90]=RGB(252,216,180);
	Palette[ 91]=RGB(252,232,180);
	Palette[ 92]=RGB(252,252,180);
	Palette[ 93]=RGB(232,252,180);
	Palette[ 94]=RGB(216,252,180);
	Palette[ 95]=RGB(196,252,180);
	Palette[ 96]=RGB(180,252,180);
	Palette[ 97]=RGB(180,252,196);
	Palette[ 98]=RGB(180,252,216);
	Palette[ 99]=RGB(180,252,232);
	Palette[100]=RGB(180,252,252);
	Palette[101]=RGB(180,232,252);
	Palette[102]=RGB(180,216,252);
	Palette[103]=RGB(180,196,252); // end 0..252
	Palette[104]=RGB(0,0,112);
	Palette[105]=RGB(28,0,112);
	Palette[106]=RGB(56,0,112);
	Palette[107]=RGB(84,0,112);
	Palette[108]=RGB(112,0,112);
	Palette[109]=RGB(112,0,84);
	Palette[110]=RGB(112,0,56);
	Palette[111]=RGB(112,0,28);
	Palette[112]=RGB(112,0,0);
	Palette[113]=RGB(112,28,0);
	Palette[114]=RGB(112,56,0);
	Palette[115]=RGB(112,84,0);
	Palette[116]=RGB(112,112,0);
	Palette[117]=RGB(84,112,0);
	Palette[118]=RGB(56,112,0);
	Palette[119]=RGB(28,112,0);
	Palette[120]=RGB(0,112,0);
	Palette[121]=RGB(0,112,28);
	Palette[122]=RGB(0,112,56);
	Palette[123]=RGB(0,112,84);
	Palette[124]=RGB(0,112,112);
	Palette[125]=RGB(0,84,112);
	Palette[126]=RGB(0,56,112);
	Palette[127]=RGB(0,28,112);
	Palette[128]=RGB(56,56,112);
	Palette[129]=RGB(68,56,112);
	Palette[130]=RGB(84,56,112);
	Palette[131]=RGB(96,56,112);
	Palette[132]=RGB(112,56,112);
	Palette[133]=RGB(112,56,96);
	Palette[134]=RGB(112,56,84);
	Palette[135]=RGB(112,56,68);
	Palette[136]=RGB(112,56,56);
	Palette[137]=RGB(112,68,56);
	Palette[138]=RGB(112,84,56);
	Palette[139]=RGB(112,96,56);
	Palette[140]=RGB(112,112,56);
	Palette[141]=RGB(96,112,56);
	Palette[142]=RGB(84,112,56);
	Palette[143]=RGB(68,112,56);
	Palette[144]=RGB(56,112,56);
	Palette[145]=RGB(56,112,68);
	Palette[146]=RGB(56,112,84);
	Palette[147]=RGB(56,112,96);
	Palette[148]=RGB(56,112,112);
	Palette[149]=RGB(56,96,112);
	Palette[150]=RGB(56,84,112);
	Palette[151]=RGB(56,68,112);
	Palette[152]=RGB(80,80,112);
	Palette[153]=RGB(88,80,112);
	Palette[154]=RGB(96,80,112);
	Palette[155]=RGB(104,80,112);
	Palette[156]=RGB(112,80,112);
	Palette[157]=RGB(112,80,104);
	Palette[158]=RGB(112,80,96);
	Palette[159]=RGB(112,80,88);
	Palette[160]=RGB(112,80,80);
	Palette[161]=RGB(112,88,80);
	Palette[162]=RGB(112,96,80);
	Palette[163]=RGB(112,104,80);
	Palette[164]=RGB(112,112,80);
	Palette[165]=RGB(104,112,80);
	Palette[166]=RGB(96,112,80);
	Palette[167]=RGB(88,112,80);
	Palette[168]=RGB(80,112,80);
	Palette[169]=RGB(80,112,88);
	Palette[170]=RGB(80,112,96);
	Palette[171]=RGB(80,112,104);
	Palette[172]=RGB(80,112,112);
	Palette[173]=RGB(80,104,112);
	Palette[174]=RGB(80,96,112);
	Palette[175]=RGB(80,88,112); // end 0..112
	Palette[176]=RGB(0,0,64);
	Palette[177]=RGB(16,0,64);
	Palette[178]=RGB(32,0,64);
	Palette[179]=RGB(48,0,64);
	Palette[180]=RGB(64,0,64);
	Palette[181]=RGB(64,0,48);
	Palette[182]=RGB(64,0,32);
	Palette[183]=RGB(64,0,16);
	Palette[184]=RGB(64,0,0);
	Palette[185]=RGB(64,16,0);
	Palette[186]=RGB(64,32,0);
	Palette[187]=RGB(64,48,0);
	Palette[188]=RGB(64,64,0);
	Palette[189]=RGB(48,64,0);
	Palette[190]=RGB(32,64,0);
	Palette[191]=RGB(16,64,0);
	Palette[192]=RGB(0,64,0);
	Palette[193]=RGB(0,64,16);
	Palette[194]=RGB(0,64,32);
	Palette[195]=RGB(0,64,48);
	Palette[196]=RGB(0,64,64);
	Palette[197]=RGB(0,48,64);
	Palette[198]=RGB(0,32,64);
	Palette[199]=RGB(0,16,64);
	Palette[200]=RGB(32,32,64);
	Palette[201]=RGB(40,32,64);
	Palette[202]=RGB(48,32,64);
	Palette[203]=RGB(56,32,64);
	Palette[204]=RGB(64,32,64);
	Palette[205]=RGB(64,32,56);
	Palette[206]=RGB(64,32,48);
	Palette[207]=RGB(64,32,40);
	Palette[208]=RGB(64,32,32);
	Palette[209]=RGB(64,40,32);
	Palette[210]=RGB(64,48,32);
	Palette[211]=RGB(64,56,32);
	Palette[212]=RGB(64,64,32);
	Palette[213]=RGB(56,64,32);
	Palette[214]=RGB(48,64,32);
	Palette[215]=RGB(40,64,32);
	Palette[216]=RGB(32,64,32);
	Palette[217]=RGB(32,64,40);
	Palette[218]=RGB(32,64,48);
	Palette[219]=RGB(32,64,56);
	Palette[220]=RGB(32,64,64);
	Palette[221]=RGB(32,56,64);
	Palette[222]=RGB(32,48,64);
	Palette[223]=RGB(32,40,64);
	Palette[224]=RGB(44,44,64);
	Palette[225]=RGB(48,44,64);
	Palette[226]=RGB(52,44,64);
	Palette[227]=RGB(60,44,64);
	Palette[228]=RGB(64,44,64);
	Palette[229]=RGB(64,44,60);
	Palette[230]=RGB(64,44,52);
	Palette[231]=RGB(64,44,48);
	Palette[232]=RGB(64,44,44);
	Palette[233]=RGB(64,48,44);
	Palette[234]=RGB(64,52,44);
	Palette[235]=RGB(64,60,44);
	Palette[236]=RGB(64,64,44);
	Palette[237]=RGB(60,64,44);
	Palette[238]=RGB(52,64,44);
	Palette[239]=RGB(48,64,44);
	Palette[240]=RGB(44,64,44);
	Palette[241]=RGB(44,64,48);
	Palette[242]=RGB(44,64,52);
	Palette[243]=RGB(44,64,60);
	Palette[244]=RGB(44,64,64);
	Palette[245]=RGB(44,60,64);
	Palette[246]=RGB(44,52,64);
	Palette[247]=RGB(44,48,64); // end 0..64
	Palette[248]=RGB(0,0,0);
	Palette[249]=RGB(0,0,0);
	Palette[250]=RGB(0,0,0);
	Palette[251]=RGB(0,0,0);
	Palette[252]=RGB(0,0,0);
	Palette[253]=RGB(0,0,0);
	Palette[254]=RGB(0,0,0);
	Palette[255]=RGB(0,0,0);
}

// Set the palette from the 'M0' format file data
void CPicReaderC::SetPaletteM0(void *Data,int Len)
{
	TByteRGBC *FilePalette;
	PaletteStart=(unsigned char)*((char*)Data);
	PaletteEnd=(unsigned char)*((char*)Data+1);

	FilePalette=(TByteRGBC*)((char*)Data+2);
	int cnt,max,Index;
	max=0;

	for (cnt=PaletteStart,Index=0;cnt<=PaletteEnd;cnt++,Index++)
	{
		Palette[cnt]=RGB(FilePalette[Index].R*4,FilePalette[Index].G*4,FilePalette[Index].B*4);
	}

	PaletteExists=true;
}

// Set the image from the 'X0' format file data
// Wrapper func; ended up doing nothing important but calling DecodeImage
void CPicReaderC::SetImageX0(void *Data,int Len)
{
	DecodeImage(Data,Len);
}

// decode data
void CPicReaderC::SetupDecodeTable(TDecodeTableC *DecodeTable, unsigned short &BitMask, unsigned short &DecodeTableIndex, unsigned char &BitMaskCount)
{
	// Locals
	int cnt;

	// Bitmasks for data bits
	BitMaskCount=9; // Max valid bit position
	BitMask=0x1ff; // Max valid BitMasks

	// DecodeTable base index
	DecodeTableIndex=0x100; // why 100, top bit in BitMask? - Coincedence, plan?

	// Initial DecodeTable setting: Next=end of list, PixelData count from 0..0xff over and over
	for (cnt=0;cnt<0x800;cnt++)
	{
		DecodeTable[cnt].Next=0xffff;
		DecodeTable[cnt].PixelData=cnt&0xff;
	}
}

// turn file bits into pixel bits
unsigned char CPicReaderC::GetNextPixel(int &StackTop, unsigned short &CurWordValue, unsigned char &BitMaskCount, unsigned short &BitMask,unsigned short *Stack, TDecodeTableC *DecodeTable, unsigned short *Data,unsigned char &DataBitCount,unsigned short &PrevIndex,unsigned char &PrevPixel,unsigned short &CurIndex,unsigned short &DecodeTableIndex, unsigned char &FormatFlag)
{
	unsigned char RetVal=0;
	int TempIndex;
	int Index;
	int CurBits;

	// if pixel stack is empty fill with decoded data from file
	if (StackTop==0) 
	{
		// Decode data from file buffer

		// Get current bits (?) from previous CurWordValue 
		// (which will have some already decode bits, some undecoded bits)
		// Discard known used bits, prep CurBits for more
		CurBits=CurWordValue>>(16-DataBitCount);

		// Get enough more bits from file data to be certain we have 
		// 1 full decodable bitstring
		while (DataBitCount<BitMaskCount)
		{
			CurWordValue=Data[CurIndex++]; // Get next word (Image data:next word)

			CurBits|=(CurWordValue<<DataBitCount)&0xffff;
			DataBitCount+=0x10;
		}

		// Update Databit count
		DataBitCount=DataBitCount-BitMaskCount; 

		// Get default Decode Lookup Index guesses
		Index=CurBits & BitMask;
		TempIndex=Index;

		// If default guess is invalid (or complex?) Set values to root lookup Index
		if (Index>=DecodeTableIndex)
		{
			TempIndex=DecodeTableIndex;
			Index=PrevIndex; 
			Stack[StackTop++]=PrevPixel;
		}

		// Folow DecodeTable list, adding each item's pixel to the stack until 
		// the end of the list (0xFFFF)
		while (DecodeTable[Index].Next!=0xFFFF)
		{
			Stack[StackTop++]=(Index&0xff00)+DecodeTable[Index].PixelData;
			Index=DecodeTable[Index].Next;
		}

		// Push last node's pixel data, and remember pixel in 'PrevPixel'
		PrevPixel=DecodeTable[Index].PixelData;
		Stack[StackTop++]=PrevPixel; 

		// Set Decode Table data at this position
		DecodeTable[DecodeTableIndex].Next=PrevIndex;
		DecodeTable[DecodeTableIndex].PixelData=PrevPixel;

		PrevIndex=TempIndex;

		// Move to next 'initial' index and Update Bitflags if necessary
		DecodeTableIndex++;
		if (DecodeTableIndex>BitMask)
		{
			BitMaskCount++;
			BitMask<<=1;
			BitMask|=1;
		}

		// Reset Decode Table (and drop recorded pixel lists) if previous data grows too large
		if (BitMaskCount>FormatFlag)
		{
			SetupDecodeTable(DecodeTable,BitMask,DecodeTableIndex,BitMaskCount);
		}
	}

	// Return pixel data from top of stack
	RetVal=(unsigned char)(Stack[--StackTop]);

	return RetVal;
}

// run the process turning file data into pixel data
void CPicReaderC::DecodeImage(void *FileData,int Len)
{
	// Locals
	unsigned short	*Data=(unsigned short*)FileData;

	unsigned char	RepeatCount=0; // Repeat count for RLE pixels

	unsigned char	CurPixelValue=0; // Cur/Next Pixel value
	unsigned char	TempPixelValue;	// Temp pixel holding var 

	unsigned char	FormatFlag=0; // First byte of file (some max bit value, I think)

	unsigned short	DecodeTableIndex=0; // Base DecodeTableIndex (default= 0x100) incremented for each successful data chunk

	unsigned short	CurWordValue=0; // Cur Word (Last file pointer position/size sometimes?)
	unsigned char	DataBitCount=0; // Cur 'active' bits in

	unsigned short	PrevIndex=0; // Previous Index found
	unsigned char	PrevPixel=0; // Previous Pixel value fetched 

	unsigned char	BitMaskCount=0; // Decode Table count of bits in BitMask (default=9)
	unsigned short	BitMask=0; // Decode Table bitmask maximum (default=0x1FF)
	TDecodeTableC	DecodeTable[0x800];

	unsigned short	CurIndex=0;
	unsigned short	Stack[500];
	int StackTop=0;

	int CurX;
	int CurY;

	// Temporary DC for immediate Bitmap creation
	//CDC BitmapDC;

	// Read Header Data
	Width=Data[CurIndex++]; // Get next word (Width)
	Height=Data[CurIndex++]; // Get next word (Height)
	
	// Do not do anything if image size is 0x0
	if (Width==0 || Height==0) 
	{
		return;
	}

	// Setup Decode Table: need beter size gague than "very large fixed number"
	//DecodeTable=new TDecodeTableC[0x800]; // Max Index seen so far =0x7FF

	/*
	Bitmap.DeleteObject();
	Bitmap.CreateBitmap(Width,Height,1,32,NULL);
	BitmapDC.CreateCompatibleDC(NULL);
	BitmapDC.SelectObject(&Bitmap);
	ValidBitmap=true;
	*/

	// Get X*Y buffer to store image vga-bytes in
	if (ImageData!=NULL)
	{
		delete [] ImageData;
		ImageData=NULL;
	}
	ImageDataLen=Width*Height;
	ImageData=new unsigned char[ImageDataLen];

	RepeatCount=0; // Pixel Repeat count=0
	CurPixelValue=0; // Cur Pixel value; none at first!

	// Get first data word
	CurWordValue=Data[CurIndex++]; // Get next word (Image data:first word)
	FormatFlag=CurWordValue&0xff; // First byte of Cur word
	
	if (FormatFlag>0xb) // Command is > 0xb Fix it
	{
		CurWordValue=(CurWordValue&0xff00)+0xb;
		FormatFlag=0xb;
	}

	// First word has 8 bits already used (the format flag data)
	DataBitCount=8;

	SetupDecodeTable(DecodeTable,BitMask,DecodeTableIndex,BitMaskCount);

	// Main loop: Read through file for data
	CurY=0; // For Lines loop

	for (CurY=0; CurY<Height; CurY++)
	{
		// Parse Data into line, a pixel at a time
		for (CurX=0;CurX<Width;CurX++)
		{

			// If this pixel is a repeat, do nothing (except decrease repeat count)
			if (RepeatCount>0) // "RLE" Repeat count
			{
				RepeatCount--;
			}
			else
			{
				TempPixelValue=GetNextPixel(StackTop, CurWordValue, BitMaskCount, BitMask,Stack,DecodeTable,Data,DataBitCount,PrevIndex,PrevPixel,CurIndex,DecodeTableIndex, FormatFlag);

				// If next value is not 'repeat last pixel flag' it is a new pixel
				if (TempPixelValue!=0x90)
				{
					CurPixelValue=TempPixelValue; // Set Pixel Value
				}		
				// else get the value following the repeat flag (repeat count)
				else
				{
					TempPixelValue=GetNextPixel(StackTop, CurWordValue, BitMaskCount, BitMask,Stack,DecodeTable,Data,DataBitCount,PrevIndex,PrevPixel,CurIndex,DecodeTableIndex, FormatFlag);

					// If the repeat count is 0, the 90 is a pixel value, not a rep instrution!
					if (TempPixelValue==0)
					{
						CurPixelValue=0x90;
					}
					// Otherwise, setup the repeat
					else
					{
						// Already done pixel 1 (before 90), 
						// will do pixel 2 right now, so adjust count 
						// to correct 'future repeat' values
						RepeatCount=TempPixelValue-2; 
					}
				}
			}

			// Just put the pixel in the bitmap for now
			//BitmapDC.SetPixel(CurX,CurY,GetColor(CurPixelValue)); 
			ImageData[CurY*Width+CurX]=(unsigned char)CurPixelValue;

		} // loop pixels in line (CurX)

	} // loop lines (CurY)
			
	// Cleanup Code
	//delete [] DecodeTable;
}

