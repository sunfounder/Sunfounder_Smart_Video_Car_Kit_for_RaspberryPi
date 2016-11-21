#!/usr/bin/python
import smbus
import time
import math
import RPi.GPIO as GPIO

# ============================================================================
# PCA9685 16-Channel 12-Bit I2C BUS PWM Driver
# ============================================================================

class PWM(object):
	_MODE1				= 0x00
	_MODE2				= 0x01
	_SUBADR1			= 0x02
	_SUBADR2			= 0x03
	_SUBADR3			= 0x04
	_PRESCALE			= 0xFE
	_LED0_ON_L			= 0x06
	_LED0_ON_H			= 0x07
	_LED0_OFF_L			= 0x08
	_LED0_OFF_H			= 0x09
	_ALL_LED_ON_L		= 0xFA
	_ALL_LED_ON_H		= 0xFB
	_ALL_LED_OFF_L		= 0xFC
	_ALL_LED_OFF_H		= 0xFD

	_RESTART			= 0x80
	_SLEEP				= 0x10
	_ALLCALL			= 0x01
	_INVRT				= 0x10
	_OUTDRV				= 0x04

	RPI_REVISION_0 = ["900092"]
	RPI_REVISION_1_MODULE_B = ["Beta", "0002", "0003", "0004", "0005", "0006", "000d", "000e", "000f"]
	RPI_REVISION_1_MODULE_A = ["0007", "0008", "0009",]
	RPI_REVISION_1_MODULE_BP = ["0010", "0013"]
	RPI_REVISION_1_MODULE_AP = ["0012"]
	RPI_REVISION_2 = ["a01041", "a21041"]
	RPI_REVISION_3 = ["a02082", "a22082"]

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "PCA9685.py":'

	def __init__(self, bus_number=None, address=0x40):
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
		self.set_all_value(0, 0)
		self._write_byte_data(self._MODE2, self._OUTDRV)
		self._write_byte_data(self._MODE1, self._ALLCALL)
		time.sleep(0.005)

		mode1 = self._read_byte_data(self._MODE1)
		mode1 = mode1 & ~self._SLEEP
		self._write_byte_data(self._MODE1, mode1)
		time.sleep(0.005)

	def _write_byte_data(self, reg, value):
		if self._DEBUG:
			print self._DEBUG_INFO, 'Writing value %2X to %2X' % (value, reg)
		self.bus.write_byte_data(self.address, reg, value)

	def _read_byte_data(self, reg):
		if self._DEBUG:
			print self._DEBUG_INFO, 'Reading value from %2X' % reg
		results = self.bus.read_byte_data(self.address, reg)
		return results

	def _get_bus_number(self):
		"Gets the version number of the Raspberry Pi board"
		# Courtesy quick2wire-python-api
		# https://github.com/quick2wire/quick2wire-python-api
		# Updated revision info from: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
		try:
			f = open('/proc/cpuinfo','r')
			for line in f:
				if line.startswith('Revision'):
					if line[11:-1] in self.RPI_REVISION_0:
						return 0
					elif line[11:-1] in self.RPI_REVISION_1_MODULE_B:
						return 0
					elif line[11:-1] in self.RPI_REVISION_1_MODULE_A:
						return 0
					elif line[11:-1] in self.RPI_REVISION_1_MODULE_BP:
						return 1
					elif line[11:-1] in self.RPI_REVISION_1_MODULE_AP:
						return 0
					elif line[11:-1] in self.RPI_REVISION_2:
						return 1
					elif line[11:-1] in self.RPI_REVISION_3:
						return 1
					else:
						return line[11:-1]
		except:
			f.close()
			return 'Open file error'
		finally:
			f.close()

	def set_frequency(self, freq):
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set frequency to %d' % freq
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

	def set_value(self, channel, on, off):
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set channel "%d" to value "%d"' % (channel, off)
		self._write_byte_data(self._LED0_ON_L+4*channel, on & 0xFF)
		self._write_byte_data(self._LED0_ON_H+4*channel, on >> 8)
		self._write_byte_data(self._LED0_OFF_L+4*channel, off & 0xFF)
		self._write_byte_data(self._LED0_OFF_H+4*channel, off >> 8)

	def set_all_value(self, on, off):
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set all channel to value "%d"' % (off)
		self._write_byte_data(self._ALL_LED_ON_L, on & 0xFF)
		self._write_byte_data(self._ALL_LED_ON_H, on >> 8)
		self._write_byte_data(self._ALL_LED_OFF_L, off & 0xFF)
		self._write_byte_data(self._ALL_LED_OFF_H, off >> 8)

	def set_debug(self, debug):
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print self._DEBUG_INFO, "Set debug on"
		else:
			print self._DEBUG_INFO, "Set debug off"
