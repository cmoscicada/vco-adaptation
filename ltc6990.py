############################################
##
## Engineer: Chongsoo Jung
## 
## Create Date: 2021/08/08
##
## Project name: vco-adaptation
## Target Devices: PYNQ-Z1 & AD5676 & LTC6990
## Description: Control VCO (LTC6990) with DAC. 
##
## Dependencies: 
##
## Revision 1.1 - div code finder [find_divcode()] implemented 
## Revision 1.0 - File Created 
## Additional Comments: 
##
#############################################


from pynq import Overlay
from pynq.lib import AxiGPIO
ol = Overlay("./overlays/CICADA_N_CLAIRE.bit")

import dac #dac.py in proj. vco-adaptation
import time



# V_DIV pin voltage of LTC6990 monitored by an internal 4b ADC (VDD referenced)
# DIVCODE (A/D result) programs two settings on the LTC6990:
#  1. the output freq. divieder setting (N_DIV)
#  2. the state of the output when disabled (via the Hi-Z bit)
# see the Table 1. of the LTC6990 datasheet for the details

# return the required DIVCODE 
# inputs: 
# hiz: determine the state of the output when disabled
# ndiv: division ratio 
def find_divcode(hiz, ndiv): 
    
    if(ndiv == 1):
        divcode_ndiv = 0
    elif(ndiv == 2):
        divcode_ndiv = 1
    elif(ndiv == 4):
        divcode_ndiv = 2
    elif(ndiv == 8):
        divcode_ndiv = 3
    elif(ndiv == 16):
        divcode_ndiv = 4
    elif(ndiv == 32):
        divcode_ndiv = 5
    elif(ndiv == 64):
        divcode_ndiv = 6
    elif(ndiv == 128):
        divcode_ndiv = 7
    else:
        print("invalid N_DIV variable!")
        print("N_DIV should be 1/2/4/8/16/32/64/128")
        return -1 
    
    if(hiz == 0):
        divcode_base = 0
        divcode = divcode_base + divcode_ndiv
    elif(hiz == 1):
        divcode_base = 15
        divcode = divcode_base - divcode_ndiv
    else:
        print("invalid Hi-Z variable!")
        print("Hi-Z variable should be 0 or 1")
        return -1 
     
    #print("[DEBUG] DIVCODE result: %i" %(divcode))
    
    return divcode
    
    