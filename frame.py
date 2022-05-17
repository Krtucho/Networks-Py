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
        self.index += 1
        
    def get_src_mac(self)->str:
        """Devuelve la mac de origen que pertenece a la trama"""
        if self.index >= SRC_MAC_END_INDEX:
            mac_lst = self.bits[SRC_MAC_START_INDEX:SRC_MAC_END_INDEX+1]
            return Utils.bin_to_hex("".join(mac_lst))
        return ""
        
    def get_dst_mac(self)->str:
        """Devuelve la mac de destino que pertenece a la trama"""
        if self.index >= DST_MAC_END_INDEX:
            mac_lst = self.bits[DST_MAC_START_INDEX:DST_MAC_END_INDEX+1]
            return Utils.bin_to_hex("".join(mac_lst))
        return ""
    
    def get_data_size(self)->int:
        DATA_SIZE_START_INDEX = 32
        if self.index >= DATA_SIZE_START_INDEX:
            # return int("".joint(self.bits[DATA_SIZE_START_INDEX:DATA_SIZE_START_INDEX+8]))
            return self.bits[DATA_SIZE_START_INDEX:DATA_SIZE_START_INDEX+8]
        return None
        
    def get_data_check_size(self)->int:
        DATA_CHECK_START_INDEX = 40
        if self.index >= DATA_CHECK_START_INDEX:
            # return int("".joint(self.bits[DATA_CHECK_START_INDEX:DATA_CHECK_START_INDEX+8]))
            return self.bits[DATA_CHECK_START_INDEX:DATA_CHECK_START_INDEX+8]
        return None
        
    def get_data_bits(self)->list:
        DATA_START_INDEX = 48
        if self.index >= DATA_START_INDEX:
            return self.bits[DATA_START_INDEX:DATA_START_INDEX+8]
        return None
        
    def get_check_bits(self)->list:
        CHECK_START_INDEX = 48
        if self.index >= CHECK_START_INDEX:
            return self.bits[CHECK_START_INDEX:CHECK_START_INDEX+8]
        return None
    
    @staticmethod
    def parse_frame_data(data:str, method:int=1): 
        """Parsea la <data> introducida por el comando send_frame, el metodo 1 es tomar la data como los datos a enviar, el metodo 2 es obtener cada campo de la <data> justo como lo decia el pdf de la orientacion"""
        if method == 1:
            data_to_send = Utils.hex_to_bin()
            data_size = len(data_to_send)
            return data_to_send, data_size
        elif method ==2:
            data_bin = Utils.hex_to_bin(data)
            
            # Primeros 16 bits mac de origen
            src_mac = data_bin[SRC_MAC_START_INDEX:SRC_MAC_END_INDEX+1]
            
            # 16 bits mac de destino
            dst_mac = data_bin[DST_MAC_START_INDEX:DST_MAC_END_INDEX+1]
            
            # 8 bits tamaño de los datos
            data_size = Utils.bin_to_dec(data_bin[32:41])
            
            # 8 bits tamaño de datos de verificacion
            check_size = Utils.bin_to_dec(data_bin[40:49])
            
            data = data_bin[48: 48+data_size]
            
            check_data = data_bin[48+data_size: 48+data_size+check_size]
            return src_mac, dst_mac, data_size, check_size, data, check_data