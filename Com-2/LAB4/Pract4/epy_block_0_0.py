import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
    """This block is a CE VCO or baseband VCO and works as following: the first input is the amplitude, 
    while the second phase is the phase, the output is the complex envelope which has euler form """

    def __init__(self,):  
        gr.sync_block.__init__(
            self,
            name='e_CE_VCO_fc',  #block name  
            in_sig=[np.float32, np.float32], # float32 data type, the first input is the amplitude and second input is the phase
            out_sig=[np.complex64] # complex64 data type, output complex envelope.
        )
        
    def work(self, input_items, output_items): #paramenter function 
        A=input_items[0] #amplitude input
        Q=input_items[1] #phase input
        y=output_items[0] #output complex envelope.
        N=len(A)
        y[:]=A*np.exp(1j*Q) #output complex envelope, euler form.
        return len(output_items[0])
