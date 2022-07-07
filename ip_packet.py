from utils import Utils


class IP_Packet:
    def __init__(self, state="active", bits=[]) -> None:
        self.bits :list = bits
        self.index = len(self.bits) -1 if len(self.bits) > 0 else 0
    
    def add_bit(self, bit:int):
        if not(bit == -1):
            self.bits.append(bit)
            self.index += 1
            
    # def create_packet(dst_ip,src_ip,ttl,protocol,payload_size,packet_data):
    def create_packet(self,source_ip_adress,dest_ip_adress, ttl,protocol,payload_size,packet_data):#crea un paquete ip con los datos en una instruccion
        #agregar todos los bits de las cosas a los bits del ip_packet
        self.bits=source_ip_adress + dest_ip_adress+ ttl + protocol + payload_size + packet_data



    def get_dst_ip(self):
        DST_IP_END_INDEX = 31
        if self.index >= DST_IP_END_INDEX:
            return self.bits[:32]
        return None
    
    def get_src_ip(self):
        SRC_IP_END_INDEX = 63
        if self.index >= SRC_IP_END_INDEX:
            return self.bits[32:64]
        return None
    
    def get_ttl(self):
        TTL_END_INDEX = 71
        if self.index >= TTL_END_INDEX:
            return self.bits[64:72]
        return None
    
    def get_protocol(self):
        PROT_END_INDEX = 79
        if self.index >= PROT_END_INDEX:
            return self.bits[72:80]
        return None
    
    def get_payload_size(self):
        PAYLOAD_END_INDEX = 87
        if self.index >= PAYLOAD_END_INDEX:
            return self.bits[80:88]
        return None
    
    def calc_data_size(self):
        bits = self.get_payload_size()
        if bits == None:
            return None
        return Utils.bin_to_dec("".join([str(v) for v in bits]))
    
    def get_packet_data(self):
        PACKET_DATA_START_INDEX = 88
        if self.index >= PACKET_DATA_START_INDEX:
            return self.bits[88:]
        return None
    
    def has_finished_receiving(self):
        data_length = self.calc_data_size()
        if data_length == None:
            return False
        return self.index >= data_length + 88
    
    def convert_from_bits_to_ip(bits):
        """Devuelve una lista con 4 numeros 1 para cada posicion de la ip"""
        if len(bits) < 32:
            return None
        return [Utils.bin_to_dec("".join([str(v) for v in bits[:8]])),
         Utils.bin_to_dec("".join([str(v) for v in bits[8:16]])),
         Utils.bin_to_dec("".join([str(v) for v in bits[16:24]])),
         Utils.bin_to_dec("".join([str(v) for v in bits[24:32]]))
         ]

 
    def create_icmp_packet(self,payload:int,src_ip:str,dest_ip:str):
        _, dest_ip_tr = Utils.ip_str_to_ip_bit(dest_ip)
        _, src_ip_tr =  Utils.ip_str_to_ip_bit(src_ip)
        last = [int(v) for v in Utils.dec_to_bin(payload)]
        bits = dest_ip_tr + src_ip_tr + [0,0,0,0,0,0,0,0] + [0,0,0,0,0,0,0,1] + [0,0,0,0,0,0,0,1] + last
        self.bits=bits

