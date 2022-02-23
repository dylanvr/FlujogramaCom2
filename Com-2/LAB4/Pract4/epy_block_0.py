import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  
    """This block is a RF VCO and works as following: the first input is the amplitude and the second input is the phase 
    and the output is the modulated signal s(t) bandpass, it has two parameters: carrier frequency, and samp rate"""

    def __init__(self, fc=128000, samp_rate=320000):  
        gr.sync_block.__init__(
            self,
            name='e_RF_VCO_ff',   # block name 
            in_sig=[np.float32, np.float32], # float32 data type, the first input is the amplitude and second input is the phase  
            out_sig=[np.float32] #floar32 data type, is modulated signtal s(t)
        )
        self.fc = fc #assing parameter fc 
        self.samp_rate = samp_rate #assing parameter samp_rate
        self.n_m=0 

    def work(self, input_items, output_items): #paramenter function 
        A=input_items[0] #amplitude input
        Q=input_items[1] #phase input 
        y=output_items[0] #Base band signal output 
        N=len(A)# vector width (Amplitude)
        n=np.linspace(self.n_m,self.n_m+N-1,N) #dicretize the vector 
        self.n_m += N
        y[:]=A*np.cos(2*math.pi*self.fc*n/self.samp_rate+Q) #output bass band signal
        return len(output_items[0])


