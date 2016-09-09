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

	_BUS_0_TYPES = ['Pi 1 Model B']
	_BUS_1_TYPES = ['Pi 3 Model B', 'Pi 2 Model B', 'Model B+']

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "PCA9685.py":'

	def softwareReset(cls):
		if self._DEBUG:
			print self._DEBUG_INFO, "Reset"
		cls.general_call_i2c.writeRaw8(0x06)

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
		pi_type = GPIO.RPI_INFO['TYPE']
		if pi_type in self._BUS_0_TYPES:
			bus_number = 0
		elif pi_type in self._BUS_1_TYPES:
			bus_number = 1
		else:
			raise ValueError("Reading Pi type error, Your Pi {0} is not in the list".format(pi_type))

		if self._DEBUG:
			print self._DEBUG_INFO, 'Get i2c bus number %d' % bus_number
		return bus_number

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

		self.set_debug(self._DEBUG)

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
