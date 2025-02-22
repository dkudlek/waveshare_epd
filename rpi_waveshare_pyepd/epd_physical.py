# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-06-21
# * | Info        :
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import spidev
import RPi.GPIO as GPIO
import time

# Pin definition
RST_PIN         = 17
DC_PIN          = 25
CS_PIN          = 8
BUSY_PIN        = 24

# SPI device, bus = 0, device = 0
SPI = spidev.SpiDev(0, 0)
#SPI.no_cs = True

def epd_digital_write(pin, value):
    GPIO.output(pin, value)

def epd_digital_read(pin):
    return GPIO.input(BUSY_PIN)

def epd_delay_ms(delaytime):
    time.sleep(delaytime / 1000.0)

def spi_transfer(data):
    SPI.writebytes(data)

def epd_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(RST_PIN, GPIO.OUT)
    GPIO.setup(DC_PIN, GPIO.OUT)
    GPIO.setup(CS_PIN, GPIO.OUT)
    GPIO.setup(BUSY_PIN, GPIO.IN)
    SPI.max_speed_hz = 2000000
    SPI.mode = 0b00
    return 0

def is_busy():
    val = epd_digital_read(BUSY_PIN)
    if val == 0:
        return True
    else:
        return False

def reset_low():
    epd_digital_write(RST_PIN, GPIO.LOW)

def reset_high():
    epd_digital_write(RST_PIN, GPIO.HIGH)

def send_command(command):
    epd_digital_write(DC_PIN, GPIO.LOW)
    # the parameter type is list but not int
    # so use [command] instead of command
    spi_transfer([command])

def send_data(data):
    epd_digital_write(DC_PIN, GPIO.HIGH)
    # the parameter type is list but not int
    # so use [data] instead of data
    spi_transfer([data])

def epd_exit():
    print("spi end")
    SPI.close()

    print("close 5V, Module enters 0 power consumption ...")
    GPIO.output(RST_PIN, 0)
    GPIO.output(DC_PIN, 0)

    GPIO.cleanup()
