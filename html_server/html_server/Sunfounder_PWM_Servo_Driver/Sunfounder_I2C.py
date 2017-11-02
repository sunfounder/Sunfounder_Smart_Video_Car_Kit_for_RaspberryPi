#!/usr/bin/python

import smbus

RPI_REVISION_0 = ["900092"]
RPI_REVISION_1_MODULE_B = ["Beta", "0002", "0003", "0004", "0005", "0006", "000d", "000e", "000f"]
RPI_REVISION_1_MODULE_A = ["0007", "0008", "0009",]
RPI_REVISION_1_MODULE_BP = ["0010", "0013"]
RPI_REVISION_1_MODULE_AP = ["0012"]
RPI_REVISION_2 = ["a01041", "a21041"]
RPI_REVISION_3 = ["a02082", "a22082"]

class Sunfounder_I2C(object):

  @staticmethod
  def getPiRevision():
    "Gets the version number of the Raspberry Pi board"
    # Courtesy quick2wire-python-api
    # https://github.com/quick2wire/quick2wire-python-api
    # Updated revision info from: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
    try:
      with open('/proc/cpuinfo','r') as f:
        for line in f:
          if line.startswith('Revision'):
            return 1 if line.rstrip()[-1] in ['2','3'] else 2
    except:
      return 0

  @staticmethod
  def getPiRevision_2():
    try:
      f = open('/proc/cpuinfo','r')
      for line in f:
        if line.startswith('Revision'):
          if line[11:-1] in RPI_REVISION_0:
            return 0
          elif line[11:-1] in RPI_REVISION_1_MODULE_B:
            return 0
          elif line[11:-1] in RPI_REVISION_1_MODULE_A:
            return 0
          elif line[11:-1] in RPI_REVISION_1_MODULE_BP:
            return 1
          elif line[11:-1] in RPI_REVISION_1_MODULE_AP:
            return 0
          elif line[11:-1] in RPI_REVISION_2:
            return 1
          elif line[11:-1] in RPI_REVISION_3:
            return 1
          else:
            return line[11:-1]
    except:
      f.close()
      return 'open file error'
    finally:
      f.close()

  @staticmethod
  def getPiI2CBusNumber():
    # Gets the I2C bus number /dev/i2c#
    return 1 if Sunfounder_I2C.getPiRevision() == 2 else 1

  @staticmethod
  def getPiI2CBusNumber2():
    # get I2C bus number from /proc/cpuinfo*
    revision = Sunfounder_I2C.getPiRevision_2()
    if revision in [2, 3]:
      return 1 
    elif revision in [0, 1]:
      return 0
    else:
      raise ValueError("Error occur while getting Pi Revision. Revision:{0}".format(revision))

  def __init__(self, address, busnum=-1, debug=False):
    self.address = address
    # By default, the correct I2C bus is auto-detected using /proc/cpuinfo
    # Alternatively, you can hard-code the bus version below:
    # self.bus = smbus.SMBus(0); # Force I2C0 (early 256MB Pi's)
    # self.bus = smbus.SMBus(1); # Force I2C1 (512MB Pi's)
    self.bus = smbus.SMBus(busnum if busnum >= 0 else Sunfounder_I2C.getPiRevision_2())
    self.debug = debug

  def reverseByteOrder(self, data):
    "Reverses the byte order of an int (16-bit) or long (32-bit) value"
    # Courtesy Vishal Sapre
    byteCount = len(hex(data)[2:].replace('L','')[::2])
    val       = 0
    for i in range(byteCount):
      val    = (val << 8) | (data & 0xff)
      data >>= 8
    return val

  def errMsg(self):
    print "Error accessing 0x%02X: Check your I2C address" % self.address
    return -1

  def write8(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    try:
      self.bus.write_byte_data(self.address, reg, value)
      if self.debug:
        print "I2C: Wrote 0x%02X to register 0x%02X" % (value, reg)
    except IOError, err:
      return self.errMsg()

  def write16(self, reg, value):
    "Writes a 16-bit value to the specified register/address pair"
    try:
      self.bus.write_word_data(self.address, reg, value)
      if self.debug:
        print ("I2C: Wrote 0x%02X to register pair 0x%02X,0x%02X" %
         (value, reg, reg+1))
    except IOError, err:
      return self.errMsg()

  def writeRaw8(self, value):
    "Writes an 8-bit value on the bus"
    try:
      self.bus.write_byte(self.address, value)
      if self.debug:
        print "I2C: Wrote 0x%02X" % value
    except IOError, err:
      return self.errMsg()

  def writeList(self, reg, list):
    "Writes an array of bytes using I2C format"
    try:
      if self.debug:
        print "I2C: Writing list to register 0x%02X:" % reg
        print list
      self.bus.write_i2c_block_data(self.address, reg, list)
    except IOError, err:
      return self.errMsg()

  def readList(self, reg, length):
    "Read a list of bytes from the I2C device"
    try:
      results = self.bus.read_i2c_block_data(self.address, reg, length)
      if self.debug:
        print ("I2C: Device 0x%02X returned the following from reg 0x%02X" %
         (self.address, reg))
        print results
      return results
    except IOError, err:
      return self.errMsg()

  def readU8(self, reg):
    "Read an unsigned byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if self.debug:
        print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
         (self.address, result & 0xFF, reg))
      return result
    except IOError, err:
      return self.errMsg()

  def readS8(self, reg):
    "Reads a signed byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if result > 127: result -= 256
      if self.debug:
        print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
         (self.address, result & 0xFF, reg))
      return result
    except IOError, err:
      return self.errMsg()

  def readU16(self, reg, little_endian=True):
    "Reads an unsigned 16-bit value from the I2C device"
    try:
      result = self.bus.read_word_data(self.address,reg)
      # Swap bytes if using big endian because read_word_data assumes little 
      # endian on ARM (little endian) systems.
      if not little_endian:
        result = ((result << 8) & 0xFF00) + (result >> 8)
      if (self.debug):
        print "I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg)
      return result
    except IOError, err:
      return self.errMsg()

  def readS16(self, reg, little_endian=True):
    "Reads a signed 16-bit value from the I2C device"
    try:
      result = self.readU16(reg,little_endian)
      if result > 32767: result -= 65536
      return result
    except IOError, err:
      return self.errMsg()

if __name__ == '__main__':
  try:
    bus = Sunfounder_I2C(address=0, busnum=1)
    print "Default I2C bus is accessible"
  except:
    print "Error accessing default I2C bus"
