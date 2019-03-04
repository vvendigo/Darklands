#include "catalog.h"

#include <QFile>
#include <QDir>
#include <QFileInfo>
#include <QBuffer>
#include <QVariant>
#include <QString>
#include <QRegExp>
#include "binfile.h"
#include "imcfile.h"
#include "compressedfile.h"

Catalog::Catalog(const QByteArray &aData, QString aName, BinFile *aParent)
:	BinFile(aData, aName, aData.size(), aParent)
{
	QDataStream stream(mRawData);
	stream.setByteOrder(QDataStream::LittleEndian);
	parseFileIndex(stream);

	extractFiles();
	mRawData.clear(); //don't really need to keep the data around here, it's all stored in the extracted binfiles anyway
}

Catalog::~Catalog()
{
	qDeleteAll(mFileIndex);
	mFileIndex.clear();
}

void
Catalog::parseFileIndex(QDataStream &aStream)
{
	//first byte pari is a LE uint16 with the catalog's file count
	quint16 fileCount;
	aStream >> fileCount;

	//each index entry is 24 bytes long
	for(quint16 i = 0; i < fileCount; i++)
	{
		//filename is the first 12 bytes (dos 8.3 format), if shorter than 8.3 the name is padded with trailing 0's
		char *nameString = new char[12];
		aStream.readRawData(nameString, 12);
		QString filename = QString::fromLocal8Bit(nameString, 12);
		delete[] nameString;
		
		//next 4 bytes is a timestamp stored as LE uint32 which we don't really care about. Epoch seems to be 1/1 1978, which hints that the pixel artists were on Amigas
		quint32 timestamp;
		aStream >> timestamp;

		//next four bytes : file size in bytes, stored as LE uint32
		quint32 filesize;
		aStream >> filesize;

		//last four bytes : offset in catalog to start of file data, stored as LE uint32
		quint32 offset;
		aStream >> offset;

		mFileIndex.push_back(new CatalogIndexEntry(filename.trimmed(), filesize, offset));
	}
}

void
Catalog::extractFiles()
{
	QBuffer buffer(&mRawData);
	buffer.open(QIODevice::ReadOnly);

	foreach(CatalogIndexEntry *entry, mFileIndex)
	{
		buffer.seek(entry->mStartOffset);
		if(buffer.bytesAvailable() < entry->mSize)
			continue;

		QRegExp query("[0-9]");
		QByteArray data = buffer.read(entry->mSize);
		if(entry->mName.contains(".IMC", Qt::CaseInsensitive))
		{
			ImcFile *file = new ImcFile(data, entry->mName, entry->mSize, this);
			mChildFiles.push_back(file);
		}
		else if(entry->mName.split(".").size() == 2 && entry->mName.split(".").at(1).count(query) == 3)
		{
			CompressedFile *file = new CompressedFile(data, entry->mName, entry->mSize, this);
			mChildFiles.push_back(file);
		}
		else if(entry->mName.contains(".FLC", Qt::CaseInsensitive)
			|| entry->mName.contains(".FFC", Qt::CaseInsensitive)
			|| entry->mName.contains(".NWC", Qt::CaseInsensitive)
			|| entry->mName.contains(".NFC", Qt::CaseInsensitive)
			|| entry->mName.contains(".WWC", Qt::CaseInsensitive)
			|| entry->mName.contains(".WFC", Qt::CaseInsensitive)
			|| entry->mName.contains(".FRC", Qt::CaseInsensitive)
			|| entry->mName.startsWith("LC_", Qt::CaseInsensitive))
		{
			CompressedFile *file = new CompressedFile(data, entry->mName, entry->mSize, this);
			mChildFiles.push_back(file);
		}
		else
		{
			BinFile *file = new BinFile(data, entry->mName, entry->mSize, this);
			mChildFiles.push_back(file);
		}
	}

	buffer.close();
}



void
Catalog::exportChildren(QString aPath)
{
	if(mChildFiles.size() == 0)
		return;

	QDir dir(aPath + "/" + mName + ".DIR");
	if(!dir.exists())
		dir.mkpath(dir.absolutePath());


	foreach(BinFile *file, mChildFiles)
	{
		file->save(dir.absolutePath() + "/" + file->getName());
		file->exportChildren(dir.absolutePath());
	}
}

/** static function for loading a catalog file from disk. Verifies file format(sort of), reads file and returns a Catalog object, or NULL if file is invalid
*/
Catalog *
Catalog::loadCatalogFile(QString aFilePath)
{
	QFileInfo fileInfo(aFilePath);
	QFile file(aFilePath);

	if(!file.exists())
		return NULL;
	
	if(!file.open(QIODevice::ReadOnly))
		return NULL;

	file.seek(0x02);
	QString test(file.read(12));
	QRegExp query("[A-Za-z0-9\\.\\_]");
	if(test.isEmpty() || test.trimmed().count(query) != test.trimmed().count())
		return NULL;

	file.seek(0x00);
	QByteArray data = file.readAll();
	if(data.size() == 0)
		return NULL;

	Catalog *catalog = new Catalog(data, fileInfo.fileName());
	file.close();
	return catalog;
}