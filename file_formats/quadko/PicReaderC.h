#ifndef _PICREADERC_H_DARKLANDS
#define _PICREADERC_H_DARKLANDS

// RGB Color data structure
typedef struct
{
	unsigned char R;
	unsigned char G;
	unsigned char B;
} TByteRGBC;

// Decode Table: holds lists of decoded pixel streams
typedef struct
{
	unsigned char PixelData;
	unsigned short Next;
} TDecodeTableC;

class CPicReaderC
{
public:
	CPicReaderC();
	~CPicReaderC();

	bool Load(const char *Filename);
	bool Load(void *Buf, int BufLen);

	bool IsValid() {return Valid;}

	// Image size funcs
	int GetWidth() {return Width;}
	int GetHeight() {return Height;}

	// Single Pixel Funcs
	COLORREF GetPixel(int X, int Y); // Get RGB Pixel value (can draw it immediately)
	unsigned char GetPixelByte(int X, int Y); // Get VGA palette index byte (needs color lookup to draw)

	// Full Pixel Buffer funcs
	int GetPixelData(char *Buf, int BufLen); // Get all pixels as RGB values, needs Width*Height*3 buf size, returns memory used
	int GetPixelByteData(char *Buf, int BufLen);// Get all pixels as VGA byte values, needs Width*Height buf size, returns memory used

	// Color Funcs
	COLORREF GetColor(unsigned int Index); // Get color given VGA byte value/palette index (equivalent)
	void SetColor(unsigned int Index, COLORREF NewColor); // Set palette color at specified index (manually trigger recreate bitmap if necessary)

	// File Palette Funcs
	bool HasPalette() {return PaletteExists;} // File had a palette?
	int GetPaletteStart() {return PaletteStart;} // First index of file palette
	int GetPaletteEnd() {return PaletteEnd;} // Last index of file palette


protected:
	bool Valid;

	unsigned int Width;
	unsigned int Height;
	COLORREF Palette[256];

	unsigned char *FileData;
	long FileDataLen;
	long CurFileOffset;

	unsigned char *ImageData;
	long ImageDataLen;

	int PaletteStart;
	int PaletteEnd;
	bool PaletteExists;

protected:
	void InitPalette();

	void SetPaletteM0(void *Data,int Len);
	void SetImageX0(void *Data,int Len);

	void SetupDecodeTable(TDecodeTableC *DecodeTable, unsigned short &BitMask, unsigned short &DecodeTableIndex, unsigned char &BitMaskCount);
	unsigned char GetNextPixel(int &StackTop, unsigned short &CurWordValue, unsigned char &BitMaskCount, unsigned short &BitMask,unsigned short *Stack, TDecodeTableC *DecodeTable, unsigned short *Data,unsigned char &DataBitCount,unsigned short &PrevIndex,unsigned char &PrevPixel,unsigned short &CurIndex,unsigned short &DecodeTableIndex, unsigned char &FormatFlag);
	void DecodeImage(void *FileData,int Len);
};

#endif