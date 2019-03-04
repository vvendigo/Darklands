#include "colortable.h"

#include <QDataStream>
#include <QList>

ColorTable *ColorTable::sThis = NULL;

ColorTable *
ColorTable::sInstance()
{
	if(sThis == NULL)
		sThis = new ColorTable();
	return sThis;
}

ColorTable::ColorTable()
{
	initBasePalette();
	initEnemyPal();
}

ColorTable::~ColorTable()
{
}

QVector<QRgb>
ColorTable::colorTable(int aBlock32, int aBlock48, int aBlock64)
{
	QVector<QRgb> table = mColorTable;
	QVector<QRgb> block32 = mBlock32[aBlock32];
	QVector<QRgb> block48 = mBlock48[aBlock48];
	QVector<QRgb> block64 = mBlock64[aBlock64];

	table.remove(32, 48);
	for(int i = 32; i < 80; i++)
	{
		if(i < 48)
			table.insert(i, block32.at(i - 32));
		else if(i < 64)
			table.insert(i, block48.at(i - 48));
		else
			table.insert(i, block64.at(i - 64));
	}
	if(table.size() < 256)
		return mColorTable;
	return table;
}


int
ColorTable::getBlock32Count() const
{
	return mBlock32.count();
}

int
ColorTable::getBlock48Count() const
{
	return mBlock48.count();
}

int
ColorTable::getBlock64Count() const
{
	return mBlock64.count();
}


void 
ColorTable::initBasePalette()
{
	mColorTable.resize(256);

	mColorTable[0] = qRgb(208, 228, 244); // 0 0 0
	mColorTable[1] = qRgb(0, 0, 170); // 0 0 2a
	mColorTable[2] = qRgb(0, 170, 0); // 0 2a 0
	mColorTable[3] = qRgb(0, 170, 170); // 0 2a 2a
	mColorTable[4] = qRgb(170, 0, 0); // 2a 0 0
	mColorTable[5] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[6] = qRgb(170, 85, 0); // 2a 15 0
	mColorTable[7] = qRgb(170, 170, 170); // 2a 2a 2a
	mColorTable[8] = qRgb(85, 85, 85); // 15 15 15
	mColorTable[9] = qRgb(85, 85, 255); // 15 15 3f
	mColorTable[10] = qRgb(85, 255, 85); // 15 3f 15
	mColorTable[11] = qRgb(85, 255, 255); // 15 3f 3f
	mColorTable[12] = qRgb(255, 85, 85); // 3f 15 15
	mColorTable[13] = qRgb(199, 199, 199); // 31 31 31
	mColorTable[14] = qRgb(255, 255, 85); // 3f 3f 15
	mColorTable[15] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[16] = qRgb(174, 93, 4); // 2b 17 1
	mColorTable[17] = qRgb(186, 85, 16); // 2e 15 4
	mColorTable[18] = qRgb(195, 109, 28); // 30 1b 7
	mColorTable[19] = qRgb(203, 134, 44); // 32 21 b
	mColorTable[20] = qRgb(211, 158, 60); // 34 27 f
	mColorTable[21] = qRgb(223, 182, 77); // 37 2d 13
	mColorTable[22] = qRgb(154, 235, 174); // 26 3a 2b
	mColorTable[23] = qRgb(52, 199, 174); // d 31 2b
	mColorTable[24] = qRgb(81, 101, 255); // 14 19 3f
	mColorTable[25] = qRgb(93, 121, 239); // 17 1e 3b
	mColorTable[26] = qRgb(101, 134, 227); // 19 21 38
	mColorTable[27] = qRgb(113, 146, 215); // 1c 24 35
	mColorTable[28] = qRgb(121, 154, 199); // 1e 26 31
	mColorTable[29] = qRgb(125, 154, 186); // 1f 26 2e
	mColorTable[30] = qRgb(158, 190, 231); // 27 2f 39
	mColorTable[31] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[32] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[33] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[34] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[35] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[36] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[37] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[38] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[39] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[40] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[41] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[42] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[43] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[44] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[45] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[46] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[47] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[48] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[49] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[50] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[51] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[52] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[53] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[54] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[55] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[56] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[57] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[58] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[59] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[60] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[61] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[62] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[63] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[64] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[65] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[66] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[67] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[68] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[69] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[70] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[71] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[72] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[73] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[74] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[75] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[76] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[77] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[78] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[79] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[80] = qRgb(255, 162, 101); // 3f 28 19
	mColorTable[81] = qRgb(85, 85, 85); // 15 15 15
	mColorTable[82] = qRgb(56, 56, 56); // e e e
	mColorTable[83] = qRgb(36, 36, 36); // 9 9 9
	mColorTable[84] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[85] = qRgb(138, 0, 0); // 22 0 0
	mColorTable[86] = qRgb(162, 0, 0); // 28 0 0
	mColorTable[87] = qRgb(186, 0, 0); // 2e 0 0
	mColorTable[88] = qRgb(231, 219, 0); // 39 36 0
	mColorTable[89] = qRgb(247, 227, 85); // 3d 38 15
	mColorTable[90] = qRgb(0, 97, 162); // 0 18 28
	mColorTable[91] = qRgb(0, 69, 150); // 0 11 25
	mColorTable[92] = qRgb(0, 85, 150); // 0 15 25
	mColorTable[93] = qRgb(113, 0, 0); // 1c 0 0
	mColorTable[94] = qRgb(93, 0, 0); // 17 0 0
	mColorTable[95] = qRgb(69, 0, 0); // 11 0 0
	mColorTable[96] = qRgb(0, 130, 211); // 0 20 34
	mColorTable[97] = qRgb(0, 113, 186); // 0 1c 2e
	mColorTable[98] = qRgb(0, 97, 162); // 0 18 28
	mColorTable[99] = qRgb(0, 81, 138); // 0 14 22
	mColorTable[100] = qRgb(0, 69, 117); // 0 11 1d
	mColorTable[101] = qRgb(0, 52, 93); // 0 d 17
	mColorTable[102] = qRgb(0, 40, 69); // 0 a 11
	mColorTable[103] = qRgb(36, 36, 36); // 9 9 9
	mColorTable[104] = qRgb(255, 170, 117); // 3f 2a 1d
	mColorTable[105] = qRgb(77, 60, 28); // 13 f 7
	mColorTable[106] = qRgb(174, 109, 69); // 2b 1b 11
	mColorTable[107] = qRgb(150, 97, 56); // 25 18 e
	mColorTable[108] = qRgb(113, 77, 32); // 1c 13 8
	mColorTable[109] = qRgb(97, 69, 36); // 18 11 9
	mColorTable[110] = qRgb(89, 65, 32); // 16 10 8
	mColorTable[111] = qRgb(77, 60, 28); // 13 f 7
	mColorTable[112] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[113] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[114] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[115] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[116] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[117] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[118] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[119] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[120] = qRgb(255, 166, 113); // 3f 29 1c
	mColorTable[121] = qRgb(255, 158, 97); // 3f 27 18
	mColorTable[122] = qRgb(243, 150, 93); // 3c 25 17
	mColorTable[123] = qRgb(195, 195, 195); // 30 30 30
	mColorTable[124] = qRgb(178, 178, 178); // 2c 2c 2c
	mColorTable[125] = qRgb(134, 134, 134); // 21 21 21
	mColorTable[126] = qRgb(117, 117, 117); // 1d 1d 1d
	mColorTable[127] = qRgb(85, 60, 28); // 15 f 7
	mColorTable[128] = qRgb(166, 146, 146); // 29 24 24
	mColorTable[129] = qRgb(182, 113, 69); // 2d 1c 11
	mColorTable[130] = qRgb(158, 97, 56); // 27 18 e
	mColorTable[131] = qRgb(146, 93, 52); // 24 17 d
	mColorTable[132] = qRgb(117, 77, 40); // 1d 13 a
	mColorTable[133] = qRgb(93, 65, 32); // 17 10 8
	mColorTable[134] = qRgb(85, 60, 28); // 15 f 7
	mColorTable[135] = qRgb(73, 56, 24); // 12 e 6
	mColorTable[136] = qRgb(56, 44, 20); // e b 5
	mColorTable[137] = qRgb(40, 32, 12); // a 8 3
	mColorTable[138] = qRgb(117, 117, 117); // 1d 1d 1d
	mColorTable[139] = qRgb(89, 0, 0); // 16 0 0
	mColorTable[140] = qRgb(255, 186, 186); // 3f 2e 2e
	mColorTable[141] = qRgb(255, 158, 97); // 3f 27 18
	mColorTable[142] = qRgb(211, 130, 81); // 34 20 14
	mColorTable[143] = qRgb(146, 93, 52); // 24 17 d
	mColorTable[144] = qRgb(109, 73, 36); // 1b 12 9
	mColorTable[145] = qRgb(93, 65, 32); // 17 10 8
	mColorTable[146] = qRgb(134, 0, 0); // 21 0 0
	mColorTable[147] = qRgb(0, 93, 158); // 0 17 27
	mColorTable[148] = qRgb(0, 65, 113); // 0 10 1c
	mColorTable[149] = qRgb(65, 65, 255); // 10 10 3f
	mColorTable[150] = qRgb(32, 36, 255); // 8 9 3f
	mColorTable[151] = qRgb(0, 4, 255); // 0 1 3f
	mColorTable[152] = qRgb(0, 4, 231); // 0 1 39
	mColorTable[153] = qRgb(0, 4, 207); // 0 1 33
	mColorTable[154] = qRgb(0, 0, 182); // 0 0 2d
	mColorTable[155] = qRgb(0, 0, 158); // 0 0 27
	mColorTable[156] = qRgb(0, 0, 134); // 0 0 21
	mColorTable[157] = qRgb(0, 0, 113); // 0 0 1c
	mColorTable[158] = qRgb(0, 0, 89); // 0 0 16
	mColorTable[159] = qRgb(0, 0, 65); // 0 0 10
	mColorTable[160] = qRgb(162, 0, 0); // 28 0 0
	mColorTable[161] = qRgb(121, 0, 0); // 1e 0 0
	mColorTable[162] = qRgb(109, 0, 0); // 1b 0 0
	mColorTable[163] = qRgb(121, 0, 0); // 1e 0 0
	mColorTable[164] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[165] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[166] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[167] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[168] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[169] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[170] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[171] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[172] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[173] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[174] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[175] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[176] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[177] = qRgb(170, 130, 130); // 2a 20 20
	mColorTable[178] = qRgb(142, 97, 97); // 23 18 18
	mColorTable[179] = qRgb(170, 85, 40); // 2a 15 a
	mColorTable[180] = qRgb(158, 77, 40); // 27 13 a
	mColorTable[181] = qRgb(158, 56, 40); // 27 e a
	mColorTable[182] = qRgb(138, 52, 40); // 22 d a
	mColorTable[183] = qRgb(81, 0, 0); // 14 0 0
	mColorTable[184] = qRgb(97, 0, 0); // 18 0 0
	mColorTable[185] = qRgb(113, 0, 0); // 1c 0 0
	mColorTable[186] = qRgb(134, 0, 0); // 21 0 0
	mColorTable[187] = qRgb(154, 130, 109); // 26 20 1b
	mColorTable[188] = qRgb(186, 158, 134); // 2e 27 21
	mColorTable[189] = qRgb(223, 190, 158); // 37 2f 27
	mColorTable[190] = qRgb(4, 134, 20); // 1 21 5
	mColorTable[191] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[192] = qRgb(97, 60, 44); // 18 f b
	mColorTable[193] = qRgb(113, 73, 44); // 1c 12 b
	mColorTable[194] = qRgb(125, 81, 44); // 1f 14 b
	mColorTable[195] = qRgb(146, 105, 40); // 24 1a a
	mColorTable[196] = qRgb(162, 121, 36); // 28 1e 9
	mColorTable[197] = qRgb(178, 146, 32); // 2c 24 8
	mColorTable[198] = qRgb(195, 174, 20); // 30 2b 5
	mColorTable[199] = qRgb(150, 146, 109); // 25 24 1b
	mColorTable[200] = qRgb(24, 28, 44); // 6 7 b
	mColorTable[201] = qRgb(32, 36, 56); // 8 9 e
	mColorTable[202] = qRgb(40, 48, 69); // a c 11
	mColorTable[203] = qRgb(48, 60, 81); // c f 14
	mColorTable[204] = qRgb(56, 69, 93); // e 11 17
	mColorTable[205] = qRgb(65, 77, 105); // 10 13 1a
	mColorTable[206] = qRgb(69, 89, 117); // 11 16 1d
	mColorTable[207] = qRgb(81, 97, 138); // 14 18 22
	mColorTable[208] = qRgb(60, 52, 65); // f d 10
	mColorTable[209] = qRgb(77, 65, 81); // 13 10 14
	mColorTable[210] = qRgb(93, 81, 97); // 17 14 18
	mColorTable[211] = qRgb(109, 101, 113); // 1b 19 1c
	mColorTable[212] = qRgb(130, 121, 130); // 20 1e 20
	mColorTable[213] = qRgb(146, 138, 146); // 24 22 24
	mColorTable[214] = qRgb(101, 97, 105); // 19 18 1a
	mColorTable[215] = qRgb(113, 109, 113); // 1c 1b 1c
	mColorTable[216] = qRgb(24, 28, 44); // 6 7 b
	mColorTable[217] = qRgb(32, 36, 56); // 8 9 e
	mColorTable[218] = qRgb(40, 48, 69); // a c 11
	mColorTable[219] = qRgb(48, 60, 81); // c f 14
	mColorTable[220] = qRgb(56, 69, 93); // e 11 17
	mColorTable[221] = qRgb(65, 77, 105); // 10 13 1a
	mColorTable[222] = qRgb(69, 89, 117); // 11 16 1d
	mColorTable[223] = qRgb(81, 97, 138); // 14 18 22
	mColorTable[224] = qRgb(0, 0, 44); // 0 0 b
	mColorTable[225] = qRgb(4, 0, 65); // 1 0 10
	mColorTable[226] = qRgb(8, 0, 97); // 2 0 18
	mColorTable[227] = qRgb(24, 0, 125); // 6 0 1f
	mColorTable[228] = qRgb(44, 0, 150); // b 0 25
	mColorTable[229] = qRgb(73, 0, 178); // 12 0 2c
	mColorTable[230] = qRgb(101, 0, 207); // 19 0 33
	mColorTable[231] = qRgb(255, 223, 0); // 3f 37 0
	mColorTable[232] = qRgb(0, 0, 0); // 0 0 0
	mColorTable[233] = qRgb(16, 16, 24); // 4 4 6
	mColorTable[234] = qRgb(52, 52, 65); // d d 10
	mColorTable[235] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[236] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[237] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[238] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[239] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[240] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[241] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[242] = qRgb(255, 255, 255); // 3f 3f 3f
	mColorTable[243] = qRgb(142, 223, 255); // 23 37 3f
	mColorTable[244] = qRgb(134, 182, 154); // 21 2d 26
	mColorTable[245] = qRgb(162, 121, 73); // 28 1e 12
	mColorTable[246] = qRgb(186, 182, 60); // 2e 2d f
	mColorTable[247] = qRgb(36, 40, 44); // 9 a b
	mColorTable[248] = qRgb(16, 4, 0); // 4 1 0
	mColorTable[249] = qRgb(255, 138, 0); // 3f 22 0
	mColorTable[250] = qRgb(56, 65, 69); // e 10 11
	mColorTable[251] = qRgb(134, 117, 138); // 21 1d 22
	mColorTable[252] = qRgb(255, 219, 0); // 3f 36 0
	mColorTable[253] = qRgb(215, 24, 28); // 35 6 7
	mColorTable[254] = qRgb(207, 227, 243); // 33 38 3c
	mColorTable[255] = qRgb(255, 255, 255); // 3f 3f 3f
}


void
ColorTable::initEnemyPal()
{
	QByteArray data;
	//make first entries all white colors
	data = QByteArray::fromHex("603F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3FFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("903F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3FFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3F3FFF000000");
	createRgbFromString(data);

	data = QByteArray::fromHex("C03F27183C25173420142D1B01000910000C1600101C0013210017271919191515150D0D0D1111110B0B0B08080821002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F27183C25173420142D1B01010B00020F00031400041900061E001919191515150D0D0D1111110B0B0B08080821002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F27183C25173420142D1B010606060C0C0C1212121818181E1E1E1919191515150D0D0D1111110B0B0B08080821002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F27183C25173420142D1B010B08010E0A01120D021510031913041919191515150D0D0D1111110B0B0B08080821002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F27183C25173420142D1B010E00001200001701001B03002005011919191515150D0D0D1111110B0B0B08080821002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F27183C25173420142D1B010F0900140F011A15031F1D0725250C1919191515150D0D0D1111110B0B0B08080821002EFF000000");
	createRgbFromString(data);

	data = QByteArray::fromHex("90171008150F07120E06100C06001B2D00172700132100101C000C160009102525252121211D1D1D1919191515150D0D0DFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("90171008150F07120E06100C061427141122110F1D0F0C180C091309070E072525252121211D1D1D1919191515150D0D0DFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("90171008150F07120E06100C06211A111C170E17130C13100A0E0C070A09052525252121211D1D1D1919191515150D0D0DFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("90171008150F07120E06100C06280D0D230B0B1E09091907071405051004042525252121211D1D1D1919191515150D0D0DFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("90171008150F07120E06100C062929292424242020201B1B1B1717171313132525252121211D1D1D1919191515150D0D0DFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("90171008150F07120E06100C06192828152323121E1E0F19190C1414090F0F2525252121211D1D1D1919191515150D0D0DFF000000");
	createRgbFromString(data);

	data = QByteArray::fromHex("603F2C203F27183C25173420141B1209171008150F07120E06100C0629180021130021002E21002E21002E21002E21002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("903F2C203F27183C25170000000E0E0E0A0A0A0606060303030000002113000B0B0B2121211C1C1C181818141414101010FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F2C2024170D1B1209171008150F07120E060401013030302525252121211D1D1D1919191515151111110D0D0D080808FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F2C2024170D1B1209171008150F07120E060401013030301E130A1B1109181008150E07130D06100B050D09040B0803FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F2C2024170D1B1209171008150F07120E060401013030302C06062604042103031C01011701011200000D0000080000FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F2C2024170D1B1209171008150F07120E060401013030303030162B2A13262410211E0E1C190B171409120F070E0B05FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F2C2024170D1B1209171008150F07120E06040101303030152A151125110D200D0A1B0A071707041204020D02010901FF000000");
	createRgbFromString(data);

	data = QByteArray::fromHex("603C38393F320A330000040D0E0A1D1506170F02140F00110F3E25173E2E1C1B0B0A210D0F250F0F2A13102E1914040101FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("603C38393F320A08151B1A131B2F292C2C2127261A2321181E3E25173E2E1C00020306080B060B10090E140B1018040101FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C01111110D0D0D2828281919192121211B1209171008150F07120E06100C060401012113001C00002100002700002D0000FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("600401010D0C080E100F141511090E0B1C00002D002D1B001C3800391600003C25172A1A10100000172F3F1B2932363B3FFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C00D0D0D1111111515151919191D1D1D2828282C2C2C3333333030302525250000003C2517003F3F002F2F3C143C3C143CFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C0070C0D080E100B11130D14160D191B1422241426291A2A2E2530331C25260000003C2517003F3F002F2F3C143C3C143CFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C01403031808081D0B0A1F0D0D230F0B2B191533201A321D15311B132C17100000003C2517003F3F002F2F3C143C3C143CFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("602D002D2700271B001C3800392828282525252121211D1D1D1919191515150D0D0D1111110B0B0B080808171008150F07FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("602D06002706001D06003606002828282525252121211D1D1D1919191515150D0D0D1111110B0B0B080808171008150F07FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("6000261C001C1300140E00311E2828282525252121211D1D1D1919191515150D0D0D1111110B0B0B080808171008150F07FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("603333333030302C2C2C2828282525252121211D1D1D1919191515150D0D0D1111110B0B0B0808080808083F271821002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F2C203F291C11111108080834201424170D1B1209171008150F07120E06100C060401012918003F3D103F3D00393600FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F2C203F291C1111110808083420141E1E1E1919191313130E0E0E090909040404000000141515003F103F0000260404FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("902D0C0139300612050A3C2517251F193A33373A31252F282234251A36131904010117111115151A211C1D272425333035FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("900808080401010E0B05100C06120E061710081B12093030301919192828283C25172A1A103C143C3C143C3C143C3C143CFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("603030302C2C2C2828282525252121211D1D1D1919191515150D0D0D1111110B0B0B04010121002E21002E21002E21002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("600B0B0B1B1209171008150F07120E06100C0630303021000021002E21002E21002E21002E21002E21002E21002E21002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C021002E21002E1B12093D3F34173F3F2F26231F1713000A06200E021604011C00002416081A0903000A0B001616001010FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("603333332F2F2F2C2C2C2828282525252121211E1E1E1B1B1B2816162312121F0E0E1B0B0B1708081306060F03030B0202FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("602828282626262424242222222020201E1E1E1C1C1C1B1B1B1919191717171515151313131111110F0F0F0D0D0D0C0C0CFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("90140F0B3031291307000000003F3D37110B0816120D2A28261D17143F003F3F003F3F003F3F003F3F003F3F003F3F003FFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("901D1B173031291307000000003F3D3B17191523211D1F282627261E3F003F3F003F3F003F3F003F3F003F3F003F3F003FFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("902D2D332A2A3128282F26262D24242B2222292020271E1E252121001E1E001C1C00191900171700141400121200101000FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("90370B043E2F0A3F19103518052B06063839313E351D1917170E0E0E1B1A1A111111151414191717000000060A0B3C143C40440503");
	createRgbFromString(data);
	data = QByteArray::fromHex("90370B043E2F0A3F19103518052B06063839313E351D1917170E0E0E1B1A1A111111151414191717000000060A0B3C143CFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("902F26231F17133931203328192B26101E0A132F191E0401011A1A2417121F130D1B0F09133D3D3A30373027313122242032340503");
	createRgbFromString(data);
	data = QByteArray::fromHex("60282528262326242124221F22201D201E1B1E1C191C1B181B191619171417151215131013110F110F0D0F0D0B0D0C0A0CFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("603314143113133013132F13132E12122C12122B12122A1111291111281010261010251010240F0F230F0F210E0E200E0E484E0503");
	createRgbFromString(data);
	data = QByteArray::fromHex("901F0D0D1E0D0D1D0C0C1B0C0C1A0B0B190B0B180A0A160A0A1509091409091308081208081007070F07070E06060D0606484E0503");
	createRgbFromString(data);
	data = QByteArray::fromHex("C02828282424242020201C1C1C1818181414141010100C0C0C210C0C1A0A0A1408080E06061408081A0A0A210C0C2C002D484E0503");
	createRgbFromString(data);
	data = QByteArray::fromHex("60162B1115291014281014270F13260F13250E12240E11220D11210D10200C0F1F0C0F1E0B0E1D0B0D1C0A0D1A0A0C1909484E0503");
	createRgbFromString(data);
	data = QByteArray::fromHex("900C18090B17080A16080A1507091307091206081106071005070F05060E04060C04050B03040A03040903030802030702484E0503");
	createRgbFromString(data);
	data = QByteArray::fromHex("C01F1F1F1C1C1C1919191616161414141111110E0E0E0C0C0C0C1809081206050D04030802050D040812060C18092C002D484E0503");
	createRgbFromString(data);
	data = QByteArray::fromHex("C01F1F1F1C1C1C1919191616161414141111110E0E0E0C0C0C0C1809081206050D04030802050D040812060C18092C002DFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C01F1F1F1C1C1C1919191616161414141111110E0E0E0C0C0C0C1809081206050D04030802050D040812060C18092C002DFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("602C1E17340C080E21151C2429192125171D22141A1E12171B1014170D11140B0E10080B0D06080904050601020200000032340503");
	createRgbFromString(data);
	data = QByteArray::fromHex("90270C0A2E17133F37343333333C3F301F09023D13043A30003A30002C2C322D262D2921222C3A36263433212C2E1C242932340503");
	createRgbFromString(data);
	data = QByteArray::fromHex("602021002425022829072C2D0D30311334351A3939223D3D2B39392335361C3232162E2F102A2B0A272806232402202100202F0303");
	createRgbFromString(data);
	data = QByteArray::fromHex("C029261D1F19111C160E181308120E06342F262F2B2308050521002E21002E21002E21002E21002E21002E21002E21002EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("6028211E231E19150E0D201A15130C0A110A071C150F1A140D19120B18110A18110A150F073C143C3C143C3C143C3C143CFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("601A1A1818181516161215150F13130C11110A1010080E0E060C0C050B0B03090902070701060600040400020200010100FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("603F2E243C2B213A291F37271D35251B3223193021172D1F152B1D13281B1226191023170E21150D1F130B1C110A1A1009FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("902D1B012A19012718022517022215032014031D13031A1103170F03150E03120C03100A020D09020B0702080501060401FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C01F1F1F1C1C1C1919191616161414141111110E0E0E0C0C0C27130A231108200F061D0E051A0C04170B03140902110801FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C01000001500001600001B00000D06001300000B0000110A003F2A173331002D2B002727002121001C1B00161500101000FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("602B2524362F2C2322150F09041C1B0E16170B1212070D0E0527180E1D130A171008150F073C143C3C143C3C143C3C143CFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("60012000011F00011E00011D00011C00011B00011A00001A00001900001800001700001600001500001400001300001300404F0903");
	createRgbFromString(data);
	data = QByteArray::fromHex("90001200001100001000000F00000E00000D00000C00000C00000B00000A00000900000800000700000600000500000500404F0903");
	createRgbFromString(data);
	data = QByteArray::fromHex("C03F1300380E00320A002C07002604002002001A00001400001400001A00002002002604002C0700320A00380E003F1300404F0903");
	createRgbFromString(data);
	data = QByteArray::fromHex("60300E002D0B01290A022608042307052006061D07081A070917070A14070A11070A000E0B001511231200291900003F00FF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("903F3B263C361C393114362C0C3327053022000D05060F0707120909150B0B170E0D1A11101C14131F1716221B1A241F1EFF000000");
	createRgbFromString(data);
	data = QByteArray::fromHex("C02723222A27263F3D373A342F21190C2D1C1C2A1D16391E0A35190A341708341607331406331305321103310F01300E00FF000000");
	createRgbFromString(data);
}

void
ColorTable::createRgbFromString(const QByteArray &aData)
{
	QDataStream stream(aData);
	QVector<QRgb> colors;
	quint8 block;
	stream >> block;
	for(int i = 0; i < 16; i++)
	{
		quint8 red, green, blue;
		stream >> red >> green >> blue;
		//the bitshifts below are how you convert from 6bit channel to 8 bit
		colors.push_back(qRgb((red << 2) | (red >> 4), (green << 2) | (green >> 4), (blue << 2) | (blue >> 4)));
	}

	if(block == 0x60)
		mBlock32[mBlock32.size()] = colors;
	if(block == 0x90)
		mBlock48[mBlock48.size()] = colors;
	if(block == 0xC0)
		mBlock64[mBlock64.size()] = colors;
}