"""
VCNL4010 Module
THIS IS NOT THREAD SAFE SO WATCH OUT !
"""
import i2c

"""  VCNL4010 I2C  parameters """
VCNL4010_ADDR = 0x13

"""  VCNL4010 Registers addresses  """
VCNL4010_CMD_REG = 0x80
VCNL4010_ID_REG = 0x81
VCNL4010_PROXRATE_REG = 0x82
VCNL4010_IRCUR_REG = 0x83

"""  VCNL4010 Ambient light registers  """
VCNL4010_ALPARMA_REG = 0x84
VCNL4010_ALVH_REG = 0x85
VCNL4010_ALVL_REG = 0x86

"""  VCNL4010 Proximity registers  """
VCNL4010_PMH_REG = 0x87
VCNL4010_PML_REG = 0x88

"""  VCNL4010 Interrupt registers  """
VCNL4010_INTCTR_REG = 0x89
VCNL4010_LTHRSH_REG = 0x8A
VCNL4010_LTHRSL_REG = 0x8B
VCNL4010_HTHRSH_REG = 0x8C
VCNL4010_HTHRSL_REG = 0x8B
VCNL4010_INTSTS_REG = 0x8E

"""  VCNL4010 Proximity Modulator Timing Adj register  """
VCNL4010_PMTA_REG = 0x8F


class VCNL4010:
    def __init__(self, port):
        self.port = port
        #Set port address to the VCNL4010 adress
        self.port.set_addr(VCNL4010_ADDR)
        #Write to command register
        self.port.write([VCNL4010_CMD_REG, 0x80])
        #Write to ambient light param. register
        self.port.write([VCNL4010_ALPARMA_REG, 0x9D])
        #Write to interrupt control register
        self.port.write([VCNL4010_INTCTR_REG, 0x00])
    
    def getAmbientLight(self):
        #Set port address to the VCNL4010 adress in case
        #other devices changed it
        self.port.set_addr(VCNL4010_ADDR)
        dataRdy = False
        #Trigger a one shot ambient light measurement
        self.port.write([VCNL4010_CMD_REG, 0x90])
        #Wait until ambient light data is ready
        while(not dataRdy):
            t = self.port.write_read(VCNL4010_CMD_REG, 1)
            if(t[0] & 0x40):
                dataRdy = True
        #Read ambient light from both the high and low registers
        data = self.port.write_read(VCNL4010_ALVH_REG, 2)
    
        ret = (data[0] << 8 | data[1])*0.25
    
        return ret
    
    def getProximity(self):
        #Set port address to the VCNL4010 adress in case
        #other devices changed it
        self.port.set_addr(VCNL4010_ADDR)
        dataRdy = False
        #Trigger a one shot proximity measurement
        self.port.write([VCNL4010_CMD_REG, 0x88])
        #Wait until proximity data is ready
        while(not dataRdy):
            t = self.port.write_read(VCNL4010_CMD_REG, 1)
            if(t[0] & 0x20):
                dataRdy = True
        #Read proximity from both the high and low registers
        data = self.port.write_read(VCNL4010_PMH_REG, 2)
    
        ret = data[0] << 8 | data[1]
    
        return ret
    
    def getLightAndProx(self):
        #Set port address to the VCNL4010 adress in case
        #other devices changed it
        self.port.set_addr(VCNL4010_ADDR)
        dataRdy = False
        #Trigger a one Shot proximity abd ambient light measurement
        self.port.write([VCNL4010_CMD_REG, 0x98])
        #Wait until proximity data is ready by anding the als_data_rdy
        #and prox_data_rdy with 0x60 mask
        while(not dataRdy):
            t = self.port.write_read(VCNL4010_CMD_REG, 1)
            if(t[0] & 0x60):
                dataRdy = True
        #Read proximity and ambiet lights
        data = self.port.write_read(VCNL4010_ALVH_REG, 4)
        
        light = (data[0] << 8 | data[1])*0.25
        prox = data[2] << 8 | data[3]
        
        return light, prox
        
        