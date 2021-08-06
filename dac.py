from pynq import Overlay
from pynq.lib import AxiGPIO
ol = Overlay("./overlays/CICADA_N_CLAIRE.bit")

import time

##Revsied from ldo.py 

vref_val = 5000 # voltage reference value in mV
dac_fs_bin = 65535
one_us = 1/1000000

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#print(color.BOLD + 'Hello World !' + color.END)

trig_ldo_dut_ip = ol.ip_dict['gpio_spi_trig_ldo_dut']
ldo_tx_rx_data_ip = ol.ip_dict['gpio_spi_ldo_tx_rx_data']
ldo_brd_sel_ts_trig_ip = ol.ip_dict['gpio_spi_ldo_brd_sel_ts_trig']

trig_ldo = AxiGPIO(trig_ldo_dut_ip).channel1
ldo_tx_data = AxiGPIO(ldo_tx_rx_data_ip).channel1
ldo_rx_data = AxiGPIO(ldo_tx_rx_data_ip).channel2
ldo_brd_sel = AxiGPIO(ldo_brd_sel_ts_trig_ip).channel1

def dac_send_trig():
    trig_val = trig_ldo.read()
    #print('prev trig val: %i' %(trig_val))
    trig_ldo.write(trig_val^1,0xf)
    trig_val = trig_ldo.read()
    #print('current trig val: %i' %(trig_val))
    
def dac_w_single_wc(): #dac write with command 
    brd_num = int(input("target brd number (0 ~ 3): "))
    if (brd_num == 0):
        vref = vref_val
    elif (brd_num == 1):
        vref = vref_val
    else:
        print("ERROR: invalid board number!")
        return -1
    
    addr = int(input("target addr.: "))
    if(addr > 7):
        print("ERROR: invalid address value!")
        return -1
    
    volt = float(input("target voltage(e.g. 400.1mV --> 400.1: "))
    if((volt)>vref):
        print("WARINING: input voltage EXCEEDS the VREF level of the DAC!")
        dac_data = dac_fs_bin
        #print('[DEBUG] vref value: %f' %(vref))
        #print('[DEBUG] input voltage value: %f' %(volt))
    else:
        #print('[DEBUG] vref value: %f' %(vref))
        #print('[DEBUG] input voltage value: %f' %(volt))
        dac_data = ((volt)/vref)*dac_fs_bin
            
    
    dac_packet = (3<<20) + (addr<<16) + int(dac_data)
    print('dac packet: %i' %(dac_packet))    
    print('dac packet in Hex: %X' %(dac_packet))
    
    ldo_brd_sel.write(brd_num,0xff)
    ldo_tx_data.write(dac_packet,0xffffff)
    dac_send_trig()

def dac_w_single(brd_num, addr, volt): #dac write
    #print('brd_num: %i addr: %i volt: %f mV'%(brd_num, addr, volt))
    if (brd_num == 0):
        vref = vref_val
    elif (brd_num == 1):
        vref = vref_val
    else:
        print("ERROR: invalid board number!")
        return -1
    
    if(addr > 7):
        print("ERROR: invalid address value!")
        return -1
    
    if((volt)>vref):
        print("WARINING: input voltage EXCEEDS the VREF level of the DAC!")
        dac_data = dac_fs_bin
    else:
        dac_data = ((volt)/vref)*dac_fs_bin
    
    #print ('dac_w_data: %d' %(dac_w_data))
    dac_packet = (3<<20) + (addr<<16) + int(dac_data)
    #print('dac packet: %i' %(dac_packet))    
    #print('dac packet in Hex: %X' %(dac_packet))
    
    ldo_brd_sel.write(brd_num,0xf)
    ldo_tx_data.write(dac_packet,0xffffff)
    dac_send_trig()    
    
def read_single(brd_num, addr): ## read dac
    if (brd_num == 0):
        vref = vref_val
    elif (brd_num == 1):
        vref = vref_val
    else:
        print("ERROR: invalid board number!")
        return -1
        
    if(addr > 7):
        print("ERROR: invalid address value!")
        return -1
    
    #set board to be read 
    ldo_brd_sel.write(brd_num,0xf)
    time.sleep(100*one_us) #wait 100us
    
    #make spi packet (read instruction)
    #command: 1001 (setup redback reg.) 
    rd_inst_packet = (9<<20) + (addr<<16) + 0
    ldo_tx_data.write(rd_inst_packet,0xffffff)
    dac_send_trig()
    time.sleep(10*one_us) #wait 10us
    
    #make read packet (NOP mode)
    #command: 0000 (no operation)
    rd_inst_packet = (0<<20) + (addr<<16) + 0
    ldo_tx_data.write(rd_inst_packet,0xffffff)
    dac_send_trig()
    time.sleep(10*one_us) #wait 10us
    
    #read readback data and print
    rb_data_raw = ldo_rx_data.read()%0x10000
    #print("debug: rb_data_raw in Hex: ", hex(rb_data_raw))
    
    rb_data_mv = 0.0
    if(brd_num == 0):
        rb_data_mv = (rb_data_raw/dac_fs_bin)*vref_val
    elif(brd_num == 1):
        rb_data_mv = (rb_data_raw/dac_fs_bin)*vref_val
    
    #print("Current voltage: ",0.2f(rb_data_mv),"mV","      ","board: ",brd_num,"addr: ",addr, )
    print("Current voltage: %0.3fmV   [brd num: %i & addr.: %i]" %(rb_data_mv, brd_num, addr) )
    
    return rb_data_mv
    


    
    