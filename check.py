# from frame import Frame
from xmlrpc.client import Boolean
from utils import Utils
from crc import CrcCalculator, Crc8

class Check:
    def __init__(self, method="CRC") -> None:
        self.method = method
    
    @staticmethod  
    # def check_frame_len(frame:Frame):
    #     return len(frame.bits) == frame.data_size + 48 + frame.get_data_check_size()
              
    # @staticmethod  
    def check(data, check_bits)->Boolean:
        # if not self.check_frame_len(frame):
        #     return False
        
        data = bytes(data)
        expected_checksum = Utils.bin_to_dec("".join([str(v) for v in check_bits])) #Utils.parse_hex_value_for_check(Utils.bin_to_hex("".join([str(v) for v in check_bits])))
        crc_calculator = CrcCalculator(Crc8.CCITT)
        checksum =  crc_calculator.calculate_checksum(data)
        #Utils.bin_to_dec("".join([str(v) for v in check_bits]))#= crc_calculator.calculate_checksum(data)
        first =  expected_checksum == checksum
        return first #and crc_calculator.verify_checksum(data, expected_checksum)
        
    @staticmethod
    def create_check_bits(data:str):
        expected_checksum = Utils.bin_to_hex(data)
        data = bytes([int(v) for v in data])
        crc_calculator = CrcCalculator(Crc8.CCITT)
        checksum = crc_calculator.calculate_checksum(data)
        return Utils.dec_to_bin(checksum)

        
# data = bytes([0, 1, 2, 3, 4, 5 ])
# data = bytes([0, 1, 1,0,1,0,1,0 ])
# print(data)
# # print(int(data))
# expected_checksum = 0xBC
# crc_calculator = CrcCalculator(Crc8.CCITT)

# checksum = crc_calculator.calculate_checksum(data)

# print( checksum == expected_checksum)
# print(hex(checksum).upper())
# print(crc_calculator.verify_checksum(data, expected_checksum))
        
#         return False