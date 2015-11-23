import io, struct, os

"""
Usage:

Open a file in binary mode
> file = TypeCastReader(open('file.esf', 'rb'))

Read some bytes 
>version = file.read(2)

Read something as a 32 bit integer
>number = file.readInt()
"""

# All defs little endian unless otherwise stated.
class TypeCastReader(io.BufferedReader): #inherits read, write, peek etc from buffered reader.
    def readByte(self):
        return(struct.unpack("B",self.read(1))[0]) #8 bit
    def readInt(self):
        return(struct.unpack("i",self.read(4))[0]) #32 bit 
    def readUInt(self):
        return(struct.unpack("I",self.read(4))[0]) #32 bit Unsigned
    def readBUshort(self):
        return(struct.unpack(">H",self.read(2))[0]) #16 bit Big Endian
    def readShort(self):
        return(struct.unpack("h",self.read(2))[0]) #16 bit
    def readUShort(self):
        return(struct.unpack("H",self.read(2))[0]) #16 bit Unsigned
    def readFloat(self):
        return(struct.unpack("f",self.read(4))[0]) #32 bit
    def readDouble(self):
        return(struct.unpack("d",self.read(8))[0]) #64 bit
    def readBool(self):
        return(self.read(1) != b'\x00') #8 bit
    def readUTF16(self):
        length = self.readUShort()
        if length == 0: length = 1
        encodedString = self.read(length*2)
        return(encodedString.decode("UTF-16")) 
    def readASCII(self): #Assumes continuous structure. 
        length = self.readUShort()
        if length == 0: 
            length = 2
        encodedString = self.read(length)
        return(encodedString.decode("ascii"))
    def read_256(self):
        string = self.read(256 * 2)
        return (string.decode("UTF-16"))
    def read_UIntVar(self): # Variable length integer
        rv, b = 0, 0b1111111
        while b & 0x80 != 0:
            b = self.readByte()
            rv = (rv << 7) + (b & 0b01111111)
        return rv       
		
class TypeCastWriter(io.BufferedWriter):
    def writeByte(self,arg):
        self.write(struct.pack("B",arg))
    def writeInt(self,arg):
        self.write(struct.pack("i",arg))
    def writeUInt(self,arg):
        self.write(struct.pack("I",arg))
    def writeShort(self,arg):
        self.write(struct.pack("h",arg))
    def writeUShort(self,arg):
        self.write(struct.pack("H",arg))
    def writeFloat(self,arg):
        self.write(struct.pack("f",arg))
    def writeDouble(self,arg):
        self.write(struct.pack("d",arg))
    def writeBool(self,arg):
        if arg:
            self.write(b'\x01')
        else:
            self.write(b'\x00')
    def writeUTF16(self,arg):
        self.writeUShort(len(arg))
        self.write(arg.encode("UTF-16")[2:])
    def writeASCII(self,arg):
        self.writeUShort(len(arg))
        self.write(arg.encode("ascii"))
    def write_UintVar(val):
        a = val & 0x7f
        r = [a]
        val >>= 7
        while val != 0:
            r.append((val & 0x7f) | 0x80)
            val >>= 7
        r = r[::-1]
        for element in r:
            writeByte(element) 
            
            
