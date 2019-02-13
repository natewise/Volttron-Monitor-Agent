#re-download files 

import time
import board
import busio
from Adafruit_CircuitPython_ADS1x15.adafruit_ads1x15 import ads1115 as ADS
from Adafruit_CircuitPython_ADS1x15.adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}\t{:>6}".format('raw', 'V', 'I'))


while True:
	bit = chan.value
	V = chan.voltage - 1.644
	I = V/.015
	print("{:>5}\t{:>5.3f}\t{:>5.4f}".format(bit, V, I))
	time.sleep(0.5)
