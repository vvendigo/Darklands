#ifndef COLORTABLE_H
#define COLORTABLE_H

#include <QVector>
#include <QMap>
#include <QByteArray>
#include <QRgb>


/** Class for setting up and retrieving a color palette where certain index blocks are customizable.
*/
class ColorTable
{
public:
	ColorTable();
	~ColorTable();

	static ColorTable *sInstance();

	QVector<QRgb> colorTable(int aBlock32 = 0, int aBlock48 = 0, int aBlock64 = 0);

	int getBlock32Count() const;
	int getBlock48Count() const;
	int getBlock64Count() const;

private:
	void initBasePalette();
	void initEnemyPal();
	void createRgbFromString(const QByteArray &aData);

	static ColorTable *sThis;

	QVector<QRgb> mColorTable;

    QMap<int, QVector<QRgb> > mBlock32;
    QMap<int, QVector<QRgb> > mBlock48;
    QMap<int, QVector<QRgb> > mBlock64;

	Q_DISABLE_COPY(ColorTable);
};

#endif // COLORTABLE_H
