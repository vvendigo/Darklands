#ifndef FILEHELPER_H
#define FILEHELPER_H

#include <QByteArray>

/** Utility class for various file operations. For now this only contains the decompression functions for decompressing IMC and  other files using the same technique (files in BC and IMAPS.CAT also uses it). 
*/
class FileHelper
{

public:
	FileHelper();
	~FileHelper();

	void decompress(const QByteArray &aRawData, QByteArray &rRetData);

private:
	void refreshCtrl(QDataStream &rStream, quint16 &rCtrl);
	quint16 rcRight(quint16 aIn);
	quint16 rcLeft(quint16 aIn);
	quint16 scRight(quint16 aIn);
	quint16 scLeft(quint16 aIn);

	bool mCarry; //emulates the carry register flag
};

#endif // FILEHELPER_H
