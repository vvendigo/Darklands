#include "filehelper.h"

#include <QDataStream>

FileHelper::FileHelper()
:	mCarry(false)
{

}

FileHelper::~FileHelper()
{

}

/** Decompression algorithm used in IMC and other files in Darklands. Adapted from disassembly.
*/
void
FileHelper::decompress(const QByteArray &aRawData, QByteArray &rRetData)
{
	QDataStream stream(aRawData);
	stream.setByteOrder(QDataStream::LittleEndian); //all atomic values should be read little-endian

	quint16 ctrl = 0; //control word, 16bit bitmask
	quint8 dx = 0; //book-keeping for control word
	quint16 counter = 0; // counter when pattern splatting

	stream >> ctrl; //first word in file is always a control word
	dx = 16;

	while(!stream.atEnd()) //read through whole file stream or until EOF marker is found
	{
		dx--;
		if(dx == 0) //if dx = 0, time to get a new control word
		{
			dx = 16;
			refreshCtrl(stream, ctrl);
			if(stream.atEnd())
				break;
		}

		ctrl = rcRight(ctrl); //take a bit from the control mask and store it in mCarry
		if(mCarry)  // if control bit is 1, next byte is uncompressed, write directly to output stream
		{
			quint8 byte;
			stream >> byte;
			rRetData.push_back(byte);
		}
		else // if control bit is 0, next byte or word is compressed
		{
			counter = 0;
			quint16 offset = 0;

			dx--;
			if(dx == 0)
			{
				dx = 16;
				refreshCtrl(stream, ctrl);
				if(stream.atEnd())
					break;
			}

			ctrl = rcRight(ctrl); //use another bit for the compressed data to determine type of compression
			if(mCarry) //if control bit is 1, next word (2 bytes) is compresed
			{
				stream >> offset; //read the compressed word

				counter = offset & 0x0700; //The 3 lower bits of the second most significant byte is the run-length
				counter >>= 8; //right shift far enough so the run-length is aligned as LSB

				//shift the 3 lowest bits of the upper byte out of circulation, then switch the three uppermost bits on
				//this is now the offset to use
				quint16 upper = ((offset >> 3) & 0xff00) | 0xE000; 
				quint16 lower = offset & 0x00ff;
				offset = upper + lower; 

				if(counter == 0) //if the run-length is 0, it either means run-length should be larger or we are at EOF
				{
					quint8 byte; 
					stream >> byte; //read another byte
					if( byte <= 1)
						break; // if byte value is 1 or 0, we have EOF
					else 
						counter = byte + 1; //if byte is larger, use it as run-length
				}
				else
				{
					counter += 2; //always add two
				}
			}
			else //if the second control bit was 0, only the next byte is compressed
			{
				//for the compressed byte, we use another two control bits from the control mask to get the run length
				for(int i = 0; i  < 2; i++)
				{
					dx--;
					if(dx == 0)
					{
						dx = 16;
						refreshCtrl(stream, ctrl);
						if(stream.atEnd())
							break;
					}

					ctrl = rcRight(ctrl); 
					counter = (counter << 1) + mCarry;
					mCarry = false;
				}

				counter += 2; //always add two
				quint8 byte;
				stream >> byte; //read the compressed byte
				offset = 0xFF00 + byte; //the byte is only the lower byte in the offset
			}

			offset = 0xFFFF - offset; //MPS relied on integer overflow wraparound in the memory offset, lets not do that...
			//read _counter_ number of bytes in the alrady decompressed data, 
			//starting from _offset_ number of bytes from the end of the data
			//and put it at the end, replicating the pattern
			for(int i = 0; i < counter; i++)
			{
				if(offset < rRetData.size())
				{
					quint8 byte = rRetData.at(rRetData.size() - offset - 1); 
					rRetData.push_back(byte);
					
				}
			}
		}
	}	
}


/** read another control mask from the data stream, preserving the last carry flag from the spent control mask
*/
void
FileHelper::refreshCtrl(QDataStream &rStream, quint16 &rCtrl)
{
	rCtrl = scRight(rCtrl);
	rStream >> rCtrl;
	rCtrl = rcLeft(rCtrl);
}


/** rotate through carry right, emulation of the x86 assembly RCR instruction
*/
quint16
FileHelper::rcRight(quint16 aIn)
{
	bool oldCarry = mCarry;
	mCarry = aIn & 0x0001;
	quint16 retVal =  aIn >> 1;
	if(oldCarry)
		retVal |= 0x8000; //set msb
	return retVal;
}

/** rotate through carry left, emulation of the x86 assembly RCL instruction
*/
quint16
FileHelper::rcLeft(quint16 aIn)
{
	bool oldCarry = mCarry;
	mCarry = aIn & 0x8000;
	quint16 retVal =  aIn << 1;
	if(oldCarry)
		retVal |= 0x0001; //set lsb
	return retVal;
}


/** shift and carry right
*/
quint16
FileHelper::scRight(quint16 aIn)
{
	mCarry = aIn & 0x0001;
	quint16 retVal =  aIn >> 1;
	return retVal;
}


/** shift and carry left
*/
quint16
FileHelper::scLeft(quint16 aIn)
{
	mCarry = aIn & 0x8000;
	quint16 retVal =  aIn << 1;
	return retVal;
}