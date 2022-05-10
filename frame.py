from check import Check
from utils import Utils
from cfg import SRC_MAC_START_INDEX, SRC_MAC_END_INDEX, DST_MAC_START_INDEX, DST_MAC_END_INDEX

class Frame:
    def __init__(self, state="active", src_mac="", dst_mac="", data_size=0, data="", check_method="CRC")-> None:
        self.state = state # Estado actual de la trama, active si se esta transmitiendo, inactive si no se esta transmitiendo, enqueued si esta encolada, completed si se ha terminado de transmitir
        self.index = 0 # Indice actual de los bits de la trama
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.data_size = data_size
        self.data = ""
        self.check: Check = Check(check_method)
        self.bits = []
     
    def add_bit(self, bit:int):
        self.bits.append(bit)
        index += 1
        
    def get_src_mac(self)->str:
        """Devuelve la mac de origen que pertenece a la trama"""
        if index >= SRC_MAC_END_INDEX:
            mac_lst = self.bits[SRC_MAC_START_INDEX:SRC_MAC_END_INDEX+1]
            return Utils.bin_to_hex("".join(mac_lst))
        return ""
        
    def get_dst_mac(self)->str:
        """Devuelve la mac de destino que pertenece a la trama"""
        if index >= DST_MAC_END_INDEX:
            mac_lst = self.bits[DST_MAC_START_INDEX:DST_MAC_END_INDEX+1]
            return Utils.bin_to_hex("".join(mac_lst))
        return ""
    
    def get_data_size(self)->int:
        DATA_SIZE_START_INDEX = 32
        if index >= DATA_SIZE_START_INDEX:
            return int("".joint(self.bits[DATA_SIZE_START_INDEX:DATA_SIZE_START_INDEX+8]))
        return None
        
    def get_data_check_size(self)->int:
        DATA_CHECK_START_INDEX = 40
        if index >= DATA_CHECK_START_INDEX:
            return int("".joint(self.bits[DATA_CHECK_START_INDEX:DATA_CHECK_START_INDEX+8]))
        return None
        
    @staticmethod
    def parse_frame_data(data:str, method:int=1): 
        """Parsea la <data> introducida por el comando send_frame, el metodo 1 es tomar la data como los datos a enviar, el metodo 2 es obtener cada campo de la <data> justo como lo decia el pdf de la orientacion"""
        if method == 1:
            data_to_send = Utils.hex_to_bin()
            data_size = len(data_to_send)
            return data_to_send, data_size
        elif method ==2:
            # Primeros 16 bits mac de origen
            # 16 bits mac de destino
            # 8 bits tamaño de los datos
            