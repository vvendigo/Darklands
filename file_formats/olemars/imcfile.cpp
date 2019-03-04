#include "imcfile.h"

#include <QFile>
#include <QFileInfo>
#include <QDir>
#include <QString>
#include <QStringList>
#include <QBuffer>
#include <QDataStream>
#include <QMessageBox>

#include "filehelper.h"
#include "sprite.h"

ImcFile::ImcFile(const QByteArray &aRawData, QString aName, quint32 aSize, BinFile *aParent)
:	BinFile(aRawData, aName, aSize, aParent)
,	mImgDataStartOffset(0)
,	mImgDataSize(0)
,	mBlock32(0)
,	mBlock48(0)
,	mBlock64(0)
{
	FileHelper helper;
	helper.decompress(mRawData, mUncompressedData);
	parseHeader();
	extractSprites();
	mRawData.clear(); //ditch compressed data, don't need it anymore. Keeping uncompressed data as it might be desired for export
}

ImcFile::~ImcFile()
{
	mFrameIndex.clear();
}

void
ImcFile::parseHeader()
{
	if(mUncompressedData.size() == 0)
		return;

	QBuffer buffer(&mUncompressedData);
	buffer.open(QIODevice::ReadOnly);
	QDataStream stream(&buffer);
	stream.setByteOrder(QDataStream::LittleEndian);

	if(mName.contains("DY", Qt::CaseInsensitive))
		buffer.seek(0x3e);
	else
		buffer.seek(0x52);

	stream >> mImgDataSize; //size of data section
	if(mImgDataSize > mUncompressedData.size())
	{
		buffer.close();
		QMessageBox::warning(NULL, "Corrupt file detected", "Sprite file " + mName + " appears to be corrupted.\nUncompressed size is smaller than indicated image data size.");
		return;
	}
	mImgDataStartOffset = mUncompressedData.size() - mImgDataSize; //start of data section

	QList<quint16> lineOffsets;
	while(buffer.pos() != mImgDataStartOffset && lineOffsets.size() <= 200)
	{
		quint16 offset;
		stream >> offset;
		lineOffsets.push_back(offset);
	}
	if(lineOffsets.size() == 200)
	{
		buffer.close();
		QMessageBox::warning(NULL, "Corrupt file detected", "Sprite file " + mName + " appears to be corrupted.");
		return;
	}

	qSort(lineOffsets);

	quint16 curLineOffset = 0;
	quint16 nextLineOffset = 0;

	for(int i = 0; i < lineOffsets.size() - 1; i++)
	{
		curLineOffset = lineOffsets.at(i);
		nextLineOffset = lineOffsets.at(i + 1);
		mFrameIndex.push_back(QPair<quint16, int>(mImgDataStartOffset + 16 * curLineOffset, 16 * (nextLineOffset - curLineOffset)));
	}
	if(lineOffsets.size() > 0)
	{
		curLineOffset = nextLineOffset;
		mFrameIndex.push_back(QPair<quint16, int>(mImgDataStartOffset + 16 * curLineOffset, mImgDataSize - 16 * curLineOffset));
	}

	buffer.close();
}


void
ImcFile::extractSprites()
{
	if(mUncompressedData.size() == 0)
		return;

	QBuffer buffer(&mUncompressedData);
	buffer.open(QIODevice::ReadOnly);

	for(int i = 0; i < mFrameIndex.count(); i++)
	{
		QPair<quint16, int> entry = mFrameIndex.at(i);
		buffer.seek(entry.first);
		QByteArray data = buffer.read(entry.second);
		if(data.size() != entry.second)
			continue;
		QString name = mName.split(".").at(0) + QString("_Sprite%1").arg(i + 1);
		Sprite *sprite = new Sprite(data, name, entry.second, this);
		if(sprite)
			mChildFiles.push_back(sprite);
	}

	buffer.close();
}


void
ImcFile::setPaletteBlocks(int aBlock32, int aBlock48, int aBlock64)
{
	if(aBlock32 != mBlock32 || aBlock48 != mBlock48 || aBlock64 != mBlock64)
	{
		mBlock32 = aBlock32;
		mBlock48 = aBlock48;
		mBlock64 = aBlock64;
		foreach(BinFile *file, mChildFiles)
		{
			if(dynamic_cast<Sprite *>(file))
				dynamic_cast<Sprite *>(file)->setPaletteBlocks(mBlock32, mBlock48, mBlock64);
		}
	}
}

void
ImcFile::retrievePaletteBlocks(int &rBlock32, int &rBlock48, int &rBlock64)
{
	rBlock32 = mBlock32;
	rBlock48 = mBlock48;
	rBlock64 = mBlock64;
}

void
ImcFile::save(QString aFileName)
{
	QFile file(aFileName);
	file.open(QIODevice::WriteOnly);
	file.write(mUncompressedData);
	file.close();
}


void
ImcFile::exportChildren(QString aPath)
{
	if(mChildFiles.size() == 0)
		return;

	QDir dir(aPath + "/" + mName + ".DIR");
	if(!dir.exists())
		dir.mkpath(dir.absolutePath());

	foreach(BinFile *file, mChildFiles)
	{
		if(dynamic_cast<Sprite *>(file))
			dynamic_cast<Sprite *>(file)->save(dir.absolutePath() + "/" + file->getName() + ".png");
	}
}


/** static function for loading an imc file from disk. Verifies file format(sort of), reads file and returns an ImcFile object, or NULL if file is invalid
*/
ImcFile *
ImcFile::loadImcFile(QString aFilePath)
{
	QFileInfo info(aFilePath);
	QFile file(aFilePath);

	if(!info.exists())
		return NULL;
	
	if(!file.open(QIODevice::ReadOnly))
		return NULL;

	QByteArray data = file.readAll();
	if(data.size() == 0)
		return NULL;

	//imc files don't have any format identifier, the closest thing we get is that they all have a specific EOF marker, 0xf0 0x00
	QByteArray tail;
	tail.push_back((char)0xf0);
	tail.push_back((char)0x00);
	if(!data.endsWith(tail)) 
		return NULL;

	ImcFile *imcfile = new ImcFile(data, info.fileName(), data.size());
	file.close();
	return imcfile;
}