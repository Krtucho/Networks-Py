from check import Check
from utils import Utils

class Frame:
    def __init__(self, state="active", src_mac="", dst_mac="", data_size=0, data="", check_method="CRC")-> None:
        self.state = state
        self.index = 0
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.data_size = data_size
        self.data = ""
        self.check: Check = Check(check_method)
        
    @staticmethod
    def parse_frame_data(data:str, method:int=1): 
        """Parsea la <data> introducida por el comando send_frame, el metodo 1 es tomar la data como los datos a enviar, el metodo 2 es obtener cada campo de la <data> justo como lo decia el pdf de la orientacion"""
        if method == 1:
             Utils.hex_to_bin()