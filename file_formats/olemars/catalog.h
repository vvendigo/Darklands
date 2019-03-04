#ifndef CATALOG_H
#define CATALOG_H

#include <QByteArray>
#include <QDataStream>

#include "binfile.h"

class ImcFile;


/** Simple holder for a header entry
*/
struct CatalogIndexEntry
{
	QString mName;
	quint32 mSize;
	quint32 mStartOffset;

	//convenient constructor
	CatalogIndexEntry(QString aName = QString(), quint32 aSize = 0, quint32 aStartOffset = 0) : mName(aName), mSize(aSize), mStartOffset(aStartOffset){}
};

/** Class holding a CAT file and its contents.
*/
class Catalog : public BinFile
{

public:
	Catalog(const QByteArray &aData, QString aName, BinFile *aParent = NULL);
	~Catalog();

	static Catalog *loadCatalogFile(QString aFilePath);

    void save(QString aFileName) {Q_UNUSED(aFileName); return;} //no point saving this
	void exportChildren(QString aPath);

private:
	void parseFileIndex(QDataStream &aStream);
	void extractFiles();

	QList<CatalogIndexEntry *> mFileIndex;
	//QList<BinFile *> mBinFiles;
	
};

#endif // CATALOG_H
