"""
LPS22HB Module
THIS IS NOT THREAD SAFE SO WATCH OUT !
"""

import i2c

LPS22HB_ADDR = 0x5D

CTRL_REG_1 = 0x10
CTRL_REG_2 = 0x11
CTRL_REG_3 = 0x12

STS_REG = 0x27

PRESS_H_REG = 0x2A
PRESS_L_REG = 0x29
PRESS_XL_REG = 0x28

TEMP_H_REG = 0x2C
TEMP_L_REG = 0x2B


class LPS22HB():
    
    def __init__(self, port):
        self.port = port
        self.port.set_addr(LPS22HB_ADDR)
        self.port.write([CTRL_REG_1, 0x02, CTRL_REG_2, 0x00])
    
    def getPressure(self):
        self.port.set_addr(LPS22HB_ADDR)
        
        dataRdy = False
        
        self.port.write([CTRL_REG_2, 0x01])
        
        while(not dataRdy):
            t = self.port.write_read(STS_REG, 1)
            if(t[0] & 0x01):
                dataRdy = True
        
        rawPressXL = self.port.write_read(PRESS_XL_REG, 1)
        rawPressL = self.port.write_read(PRESS_L_REG, 1)
        rawPressH = self.port.write_read(PRESS_H_REG, 1)
        
        rawPress = (rawPressXL[0] | rawPressL[0] << 8 | rawPressH[0] << 16)
        
        return rawPress/4096.0
        
    
    def getTemperature(self):
        self.port.set_addr(LPS22HB_ADDR)
        
        dataRdy = False
        
        self.port.write([CTRL_REG_2, 0x01])
        
        while(not dataRdy):
            t = self.port.write_read(STS_REG, 1)
            if(t[0] & 0x02):
                dataRdy = True
        
        rawTempL = self.port.write_read(TEMP_L_REG, 1)
        rawTempH = self.port.write_read(TEMP_H_REG, 1)
        
        rawTemp = (rawTempL[0] | rawTempH[0] << 8)
        
        return rawTemp/100.0
        
    
    def getPressAndTemp(self):
        return self.getPressure(), self.getTemperature()