"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='t_promedio',   # will show up in GRC
            in_sig=[np.float32],   #Tenemos una señal de entrada de tipo flotante 
            out_sig=[np.float32, np.float32, np.float32, np.float32, np.float32] #Tenemos 5 señales de salida de tipo flotante
       
        
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
       
        
        self.acum_anterior = 0
        self.Ntotales = 0
        self.acum_anterior1 = 0
        self.acum_anterior2 = 0
        

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        #output_items[0][:] = input_items[0] * self.example_param
        
        x = input_items[0]   #Señal de ENTRADA
        y0 = output_items[0] #Señal de salida para la MEDIA
        y1 = output_items[1] #Señal de salida para la MEDIA CUADRATICA
        y2 = output_items[2] #Señal de salida para el VALOR RMS
        y3 = output_items[3] #Señal de salida para la POTENCIA PROMEDIO
        y4 = output_items[4] #Señal desalida para la DESVIACION ESTANDAR
        
        #Calculamos el numero de muestras 
        N = len(x)
        self.Ntotales += N
        
        #MEDIA
        Acum_1 = self.acum_anterior + np.cumsum(x)
        self.acum_anterior = Acum_1[N-1]
        y0[:] = Acum_1/self.Ntotales #Calculo de la media
        
        
        #MEDIA CUADRATICA
        x2 = np.multiply(x,x)
        Acum_2 = self.acum_anterior1 + np.cumsum(x2)
        self.acum_anterior1 = Acum_2[N-1]
        y1[:] = Acum_2/self.Ntotales #Calculo de la media cuadratica
        
        #VALOR RMS
        y2[:] = np.sqrt(y1[:]) #Calculo del valor RMS
        
        #POTENCIA PROMEDIO
        y3[:] = np.power(y2[:],2) #Calculo de la potencia promedio
        
        #DESVIACION ESTANDAR
        x3 = np.multiply(x-y0,x-y0)
        Acum_3 = self.acum_anterior2 + np.cumsum(x3)
        self.acum_anterior2 = Acum_3[N-1]        
        y4[:] = np.sqrt(Acum_3/self.Ntotales) #Calculo de la desviacion estandar
        
        return len(output_items[0])
