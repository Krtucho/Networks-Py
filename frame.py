from check import Check
from utils import Utils
from cfg import SRC_MAC_START_INDEX, SRC_MAC_END_INDEX, DST_MAC_START_INDEX, DST_MAC_END_INDEX,DATA_SIZE,CHECK_SIZE
# from check impor Check

class Frame:
    def __init__(self, state="active", src_mac="", dst_mac="", data_size=0, data="", check_method="CRC", check_bits=[])-> None:
        self.state = state # Estado actual de la trama, active si se esta transmitiendo, inactive si no se esta transmitiendo, enqueued si esta encolada, completed si se ha terminado de transmitir
        self.index = -1 # Indice actual de los bits de la trama
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.data_size = data_size
        self.data = ""
        self.bits = []
        # self.check: Check = Check(check_method)
        if state == "receiving":
            self.bits = []
        else:
            self.bits = [int(v) for v in Utils.hex_to_bin(dst_mac) + 
                            Utils.hex_to_bin(src_mac) + 
                            Utils.dec_to_bin(data_size)+
                            Utils.dec_to_bin(CHECK_SIZE)+
                            data+Check.create_check_bits(data)] 
        self.check_bits = self.get_check_bits()

        self.actual_part='dest_mac'#guarda la parte de la trama que se esta completando actualmente
     
    def check_frame(self)-> bool:
        return Check.check(self.get_data_bits(), self.get_check_bits())
     
    def add_bit(self, bit:int):#agrega un bit a la trama y en caso de que se complete alguna de sus partes devuelve esta
        if not(bit==-1):
            self.bits.append(bit)
            self.index += 1
        if self.index==DST_MAC_END_INDEX:
            self.actual_part='source_mac'
            return 'dest_mac',self.get_dst_mac()
        if self.index==SRC_MAC_END_INDEX:
            self.actual_part='data_size'
            return 'source_mac',self.get_src_mac()
        if self.index==SRC_MAC_END_INDEX+DATA_SIZE:
            self.actual_part='check_size'
            return 'data_size',self.get_data_size()
        if self.index==SRC_MAC_END_INDEX+DATA_SIZE+CHECK_SIZE:
            self.actual_part='data_bits'
            return 'check_size', self.get_check_size()
        data_size = self.get_data_size_from_bits()
        check_size = self.get_check_size_from_bits()
        
        if not data_size==None:
            DATA_START_INDEX = 48
            if self.index==DATA_START_INDEX+data_size:
                self.actual_part='check_bits'
                return 'data_bits',self.get_data_bits()
            
        if not check_size == None:  
            check_bits = self.get_check_bits()
            if check_bits != None:
                CHECK_START_INDEX = self.get_data_size_from_bits()
                check_size = self.get_check_size_from_bits()
                CHECK_START_INDEX += 48
                if self.index > CHECK_START_INDEX + check_size -1:
                    return 'overflow',None

                # if self.index==SRC_MAC_END_INDEX+DATA_SIZE+CHECK_SIZE+data_size+check_size:
                self.actual_part='end'
                return 'check_bits',check_bits
        
        # if self.index==SRC_MAC_END_INDEX+DATA_SIZE+CHECK_SIZE+data_size:
        #     self.actual_part='end'
        #     return 'check_size',self.get_check_bits()

        # data_bits=self.get_data_bits()
        # if not(data_bits==None):
        #     if len(data_bits)== Utils.bin_to_dec(self.get_data_size()):
        #         return 'data_bits',data_bits
                
        # check_bits=self.get_check_bits()
        # if not(check_bits==None):
        #     if len(check_bits)== Utils.bin_to_dec(self.get_check_size()):
        #         return 'check_bits',check_bits

        return 'nothing',None

    
    def get_src_mac(self)->str:
        """Devuelve la mac de origen que pertenece a la trama"""
        if self.index >= SRC_MAC_END_INDEX:
            mac_lst = [str(v) for v in self.bits[SRC_MAC_START_INDEX:SRC_MAC_END_INDEX+1]]
            return Utils.bin_to_hex("".join(mac_lst))
        return ""
        
    def get_dst_mac(self)->str:
        """Devuelve la mac de destino que pertenece a la trama"""
        if self.index >= DST_MAC_END_INDEX:
            mac_lst = [str(v) for v in self.bits[DST_MAC_START_INDEX:DST_MAC_END_INDEX+1]]
            return Utils.bin_to_hex("".join(mac_lst))
        return ""
    
    def get_data_size(self)->int:
        DATA_SIZE_START_INDEX = 32
        if self.index >= DATA_SIZE_START_INDEX+8:
            # return int("".joint(self.bits[DATA_SIZE_START_INDEX:DATA_SIZE_START_INDEX+8]))
            return self.bits[DATA_SIZE_START_INDEX:DATA_SIZE_START_INDEX+8]
        return None
        
    def get_check_size(self)->int:
        CHECK_START_INDEX = self.get_data_size_from_bits()
        if CHECK_START_INDEX == None:
            return None
        CHECK_START_INDEX += 48
        # DATA_CHECK_START_INDEX = 40
        if self.index >= CHECK_START_INDEX:
            # return int("".joint(self.bits[DATA_CHECK_START_INDEX:DATA_CHECK_START_INDEX+8]))
            return self.bits[-8]
        return None
        
    def get_data_size_from_bits(self)->int:
        bits = self.get_data_size()
        if bits == None:
            return None
        return Utils.bin_to_dec("".join([str(v) for v in bits]))

    
    def get_check_size_from_bits(self)->int:
        bits = self.get_check_size()
        if bits == None:
            return None
        return 8
        # return Utils.bin_to_dec("".join([str(v) for v in bits]))
    
    def get_data_bits(self)->list:
        DATA_START_INDEX = 48
        if self.index >= DATA_START_INDEX:
            data_size = self.get_data_size_from_bits()
            if self.index >= DATA_START_INDEX+data_size:
                return self.bits[DATA_START_INDEX:DATA_START_INDEX+data_size]
        return None
        
    def get_check_bits(self)->list:
        CHECK_START_INDEX = self.get_data_size_from_bits()
        if CHECK_START_INDEX == None:
            return None
        CHECK_START_INDEX += 48
        if self.index >= CHECK_START_INDEX:
            check_size = self.get_check_size_from_bits()
            if self.index == CHECK_START_INDEX + check_size -1:
                return self.bits[CHECK_START_INDEX:CHECK_START_INDEX+check_size]
        return None

    def clear_frame(self):
        self.index = 0 # Indice actual de los bits de la trama
        self.src_mac = 0
        self.dst_mac = 0
        self.data_size = 0
        self.data = ""
        self.actual_part='dest_mac'
        self.bits = []
    
    @staticmethod
    def parse_frame_data(data:str, method:int=1): 
        """Parsea la <data> introducida por el comando send_frame, el metodo 1 es tomar la data como los datos a enviar, el metodo 2 es obtener cada campo de la <data> justo como lo decia el pdf de la orientacion"""
        if method == 1:
            data_to_send = Utils.hex_to_bin(data)
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