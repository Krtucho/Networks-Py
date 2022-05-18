from frame import Frame
from utils import Utils
from crc import CrcCalculator, Crc8

class Check:
    def __init__(self, method="CRC") -> None:
        self.method = method
    
    @staticmethod  
    def check_frame_len(frame:Frame):
        return len(frame.bits) == frame.data_size + 48 + frame.get_data_check_size()
              
    @staticmethod  
    def check(self, frame:Frame):
        if not self.check_frame_len(frame):
            return False
        
        data = bytes(frame.get_data_bits())
        expected_checksum = Utils.bin_to_hex(frame.get_check_bits())
        crc_calculator = crc_calculator.calculate_checksum(data)
        checksum = CrcCalculator(Crc8.CCITT)
        
        return expected_checksum == checksum and crc_calculator.verify_checksum(data, expected_checksum)
        
        
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