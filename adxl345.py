from machine import Pin, I2C
import time
import ustruct

# Minimal constants taken from the Adafruit Lib
ADXL345_ADDRESS          = 0x53
ADXL345_REG_DEVID        = 0x00 # Device ID
ADXL345_REG_DATAX0       = 0x32 # X-axis data 0 (6 bytes for X/Y/Z)
ADXL345_REG_POWER_CTL    = 0x2D # Power-saving features control
ADXL345_REG_DATA_FORMAT  = 0x31
ADXL345_REG_BW_RATE      = 0x2C
ADXL345_DATARATE_0_10_HZ = 0x00
ADXL345_DATARATE_0_20_HZ = 0x01
ADXL345_DATARATE_0_39_HZ = 0x02
ADXL345_DATARATE_0_78_HZ = 0x03
ADXL345_DATARATE_1_56_HZ = 0x04
ADXL345_DATARATE_3_13_HZ = 0x05
ADXL345_DATARATE_6_25HZ  = 0x06
ADXL345_DATARATE_12_5_HZ = 0x07
ADXL345_DATARATE_25_HZ   = 0x08
ADXL345_DATARATE_50_HZ   = 0x09
ADXL345_DATARATE_100_HZ  = 0x0A # (default)
ADXL345_DATARATE_200_HZ  = 0x0B
ADXL345_DATARATE_400_HZ  = 0x0C
ADXL345_DATARATE_800_HZ  = 0x0D
ADXL345_DATARATE_1600_HZ = 0x0E
ADXL345_DATARATE_3200_HZ = 0x0F
ADXL345_RANGE_2_G        = 0x00 # +/-  2g (default)
ADXL345_RANGE_4_G        = 0x01 # +/-  4g
ADXL345_RANGE_8_G        = 0x02 # +/-  8g
ADXL345_RANGE_16_G       = 0x03 # +/- 16g

class ADXL345:
    """ADXL345 accelerometer"""

    def __init__(self, i2c, address=ADXL345_ADDRESS):
        self.i2c = i2c
        self.address = address
        print("ADDRESS = " + str(self.address))
        if i2c.readfrom_mem(self.address, ADXL345_REG_DEVID, 1) == b'\xe5':
            i2c.writeto_mem(self.address, ADXL345_REG_POWER_CTL, '\x08') # Measurement mode ON
        else:
            raise RuntimeError('Failed to find the expected device ID register value')
       
    def read(self):
        raw = self.i2c.readfrom_mem(self.address, ADXL345_REG_DATAX0, 6)
        return ustruct.unpack('<hhh', raw)
