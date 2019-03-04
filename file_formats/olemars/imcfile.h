#ifndef IMCFILE_H
#define IMCFILE_H

#include "binfile.h"

#include <QByteArray>
#include <QBuffer>
#include <QList>
#include <QPair>


/** Class holding and decoding the contents of a compressed IMC file. Reads the header and creates Sprites from each data item.
*/
class ImcFile : public BinFile
{

public:
	ImcFile(const QByteArray &aRawData, QString aName, quint32 aSize, BinFile *aParent = NULL);
	~ImcFile();

	static ImcFile *loadImcFile(QString aFilePath);

	void setPaletteBlocks(int aBlock32, int aBlock48, int aBlock64);
	void retrievePaletteBlocks(int &rBlock32, int &rBlock48, int &rBlock64);

	void save(QString aFileName);
	void exportChildren(QString aPath);

private:
	void parseHeader();
	void extractSprites();

	quint16 mImgDataStartOffset;
	quint16 mImgDataSize;

	int mBlock32;
	int mBlock48;
	int mBlock64;

	QByteArray mUncompressedData;
    QList<QPair<quint16, int> > mFrameIndex; //first: offset second: size
	//QList<BinFile *> mSprites;
	
};

#endif // IMCFILE_H
