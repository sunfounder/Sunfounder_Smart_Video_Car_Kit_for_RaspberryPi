#!/usr/bin/python
'''
**********************************************************************
* Filename    : PCA9685.py
* Description : A driver module for PCA9685
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Version     : v1.2.0
**********************************************************************
'''

import smbus
import time
import math

class PWM(object):
    """A PWM control class for PCA9685."""
    _MODE1              = 0x00
    _MODE2              = 0x01
    _SUBADR1            = 0x02
    _SUBADR2            = 0x03
    _SUBADR3            = 0x04
    _PRESCALE           = 0xFE
    _LED0_ON_L          = 0x06
    _LED0_ON_H          = 0x07
    _LED0_OFF_L         = 0x08
    _LED0_OFF_H         = 0x09
    _ALL_LED_ON_L       = 0xFA
    _ALL_LED_ON_H       = 0xFB
    _ALL_LED_OFF_L      = 0xFC
    _ALL_LED_OFF_H      = 0xFD

    _RESTART            = 0x80
    _SLEEP              = 0x10
    _ALLCALL            = 0x01
    _INVRT              = 0x10
    _OUTDRV             = 0x04

    RPI_REVISION_0 = ["900092"]
    RPI_REVISION_1_MODULE_B = ["Beta", "0002", "0003", "0004", "0005", "0006", "000d", "000e", "000f"]
    RPI_REVISION_1_MODULE_A = ["0007", "0008", "0009",]
    RPI_REVISION_1_MODULE_BP = ["0010", "0013"]
    RPI_REVISION_1_MODULE_AP = ["0012"]
    RPI_REVISION_2 = ["a01041", "a21041"]
    RPI_REVISION_3 = ["a02082", "a22082"]

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "PCA9685.py":'

    def _get_bus_number(self):
        pi_revision = self._get_pi_revision()
        if   pi_revision == '0':
            return 0
        elif pi_revision == '1 Module B':
            return 0
        elif pi_revision == '1 Module A':
            return 0
        elif pi_revision == '1 Module B+':
            return 1
        elif pi_revision == '1 Module A+':
            return 0
        elif pi_revision == '2 Module B':
            return 1
        elif pi_revision == '3 Module B':
            return 1

    def _get_pi_revision(self):
        "Gets the version number of the Raspberry Pi board"
        # Courtesy quick2wire-python-api
        # https://github.com/quick2wire/quick2wire-python-api
        # Updated revision info from: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line.startswith('Revision'):
                    if line[11:-1] in self.RPI_REVISION_0:
                        return '0'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_B:
                        return '1 Module B'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_A:
                        return '1 Module A'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_BP:
                        return '1 Module B+'
                    elif line[11:-1] in self.RPI_REVISION_1_MODULE_AP:
                        return '1 Module A+'
                    elif line[11:-1] in self.RPI_REVISION_2:
                        return '2 Module B'
                    elif line[11:-1] in self.RPI_REVISION_3:
                        return '3 Module B'
                    else:
                        print "Error. Pi revision didn't recognize, module number: %s" % line[11:-1]
                        print 'Exiting...'
                        quit()
        except Exception, e:
            f.close()
            print e
            print 'Exiting...'
            quit()
        finally:
            f.close()

    def __init__(self, bus_number=None, address=0x40):
        '''Init the class with bus_number and address'''
        if self._DEBUG:
            print self._DEBUG_INFO, "Debug on"
        self.address = address
        if bus_number == None:
            self.bus_number = self._get_bus_number()
        else:
            self.bus_number = bus_number
        self.bus = smbus.SMBus(self.bus_number)
        if self._DEBUG:
            print self._DEBUG_INFO, 'Reseting PCA9685 MODE1 (without SLEEP) and MODE2'
        self.write_all_value(0, 0)
        self._write_byte_data(self._MODE2, self._OUTDRV)
        self._write_byte_data(self._MODE1, self._ALLCALL)
        time.sleep(0.005)

        mode1 = self._read_byte_data(self._MODE1)
        mode1 = mode1 & ~self._SLEEP
        self._write_byte_data(self._MODE1, mode1)
        time.sleep(0.005)
        self.frequency = 60

    def _write_byte_data(self, reg, value):
        '''Write data to I2C with self.address'''
        if self._DEBUG:
            print self._DEBUG_INFO, 'Writing value %2X to %2X' % (value, reg)
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except Exception, i:
            print i
            self._check_i2c()

    def _read_byte_data(self, reg):
        '''Read data from I2C with self.address'''
        if self._DEBUG:
            print self._DEBUG_INFO, 'Reading value from %2X' % reg
        try:
            results = self.bus.read_byte_data(self.address, reg)
            return results
        except Exception, i:
            print i
            self._check_i2c()

    def _check_i2c(self):
        import commands
        bus_number = self._get_bus_number()
        print "\nYour Pi Rivision is: %s" % self._get_pi_revision()
        print "I2C bus number is: %s" % bus_number
        print "Checking I2C device:"
        cmd = "ls /dev/i2c-%d" % bus_number
        output = commands.getoutput(cmd)
        print 'Commands "%s" output:' % cmd
        print output
        if '/dev/i2c-%d' % bus_number in output.split(' '):
            print "I2C device setup OK"
        else:
            print "Seems like I2C has not been set. Use 'sudo raspi-config' to set I2C"
        cmd = "i2cdetect -y %s" % self.bus_number
        output = commands.getoutput(cmd)
        print "Your PCA9685 address is set to 0x%02X" % self.address
        print "i2cdetect output:"
        print output
        outputs = output.split('\n')[1:]
        addresses = []
        for tmp_addresses in outputs:
            tmp_addresses = tmp_addresses.split(':')[1]
            tmp_addresses = tmp_addresses.strip().split(' ')
            for address in tmp_addresses:
                if address != '--':
                    addresses.append(address)
        print "Conneceted i2c device:"
        if addresses == []:
            print "None"
        else:
            for address in addresses:
                print "  0x%s" % address
        if "%02X" % self.address in addresses:
            print "Wierd, I2C device is connected. Try to run the program again. If the problem's still, email the error message to service@sunfounder.com"
        else:
            print "Device is missing."
            print "Check the address or wiring of PCA9685 servo driver, or email the error message to service@sunfounder.com"
            print 'Exiting...'
        quit()

    @property
    def frequency(self):
        return _frequency

    @frequency.setter
    def frequency(self, freq):
        '''Set PWM frequency'''
        if self._DEBUG:
            print self._DEBUG_INFO, 'Set frequency to %d' % freq
        self._frequency = freq
        prescale_value = 25000000.0
        prescale_value /= 4096.0
        prescale_value /= float(freq)
        prescale_value -= 1.0
        if self._DEBUG:
            print self._DEBUG_INFO, 'Setting PWM frequency to %d Hz' % freq
            print self._DEBUG_INFO, 'Estimated pre-scale: %d' % prescale_value
        prescale = math.floor(prescale_value + 0.5)
        if self._DEBUG:
            print self._DEBUG_INFO, 'Final pre-scale: %d' % prescale

        old_mode = self._read_byte_data(self._MODE1);
        new_mode = (old_mode & 0x7F) | 0x10
        self._write_byte_data(self._MODE1, new_mode)
        self._write_byte_data(self._PRESCALE, int(math.floor(prescale)))
        self._write_byte_data(self._MODE1, old_mode)
        time.sleep(0.005)
        self._write_byte_data(self._MODE1, old_mode | 0x80)

    def write(self, channel, on, off):
        '''Set on and off value on specific channel'''
        if self._DEBUG:
            print self._DEBUG_INFO, 'Set channel "%d" to value "%d"' % (channel, off)
        self._write_byte_data(self._LED0_ON_L+4*channel, on & 0xFF)
        self._write_byte_data(self._LED0_ON_H+4*channel, on >> 8)
        self._write_byte_data(self._LED0_OFF_L+4*channel, off & 0xFF)
        self._write_byte_data(self._LED0_OFF_H+4*channel, off >> 8)

    def write_all_value(self, on, off):
        '''Set on and off value on all channel'''
        if self._DEBUG:
            print self._DEBUG_INFO, 'Set all channel to value "%d"' % (off)
        self._write_byte_data(self._ALL_LED_ON_L, on & 0xFF)
        self._write_byte_data(self._ALL_LED_ON_H, on >> 8)
        self._write_byte_data(self._ALL_LED_OFF_L, off & 0xFF)
        self._write_byte_data(self._ALL_LED_OFF_H, off >> 8)

    def map(self, x, in_min, in_max, out_min, out_max):
        '''To map the value from arange to another'''
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        '''Set if debug information shows'''
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            print self._DEBUG_INFO, "Set debug on"
        else:
            print self._DEBUG_INFO, "Set debug off"

if __name__ == '__main__':
    import time

    pwm = PWM()
    pwm.frequency = 60
    for i in range(16):
        time.sleep(0.5)
        print '\nChannel %d\n' % i
        time.sleep(0.5)
        for j in range(4096):
            pwm.write(i, 0, j)
            print 'PWM value: %d' % j
            time.sleep(0.0003)
