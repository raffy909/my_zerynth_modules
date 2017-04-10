"""
VELM6070 Module
THIS IS NOT THREAD SAFE SO WATCH OUT !
"""
import i2c

"""  VEML6070 I2C adresses  """
VEML6070_ADDR_L = 0x38
VEML6070_ADDR_H = 0x39

class VEML6070:
    def __init__(self, port):
        self.port = port
        #Set port address to the VEML6070 control register/low data
        self.port.set_addr(VEML6070_ADDR_L)
        #init the sensor
        self.port.write([0x06])
    
    def getUV(self):
        #Set port to the high uv data address
        self.port.set_addr(VEML6070_ADDR_H)
        #Read one byte from the register
        uvH = self.port.read(1)
        #Set port to the low uv data / control register
        self.port.set_addr(VEML6070_ADDR_L)
        #Read one byte from the register
        uvL = self.port.read(1)
    
        ret = uvL[0] | uvH[0] << 8
    
        return ret