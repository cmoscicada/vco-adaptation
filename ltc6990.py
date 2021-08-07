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
## Revision 1.0 - File Created 
## Additional Comments: 
##
#############################################


from pynq import Overlay
from pynq.lib import AxiGPIO
ol = Overlay("./overlays/CICADA_N_CLAIRE.bit")

import dac #dac.py in proj. vco-adaptation
import time