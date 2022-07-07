from xmlrpc.client import Boolean
from utils import Utils
from crc import CrcCalculator, Crc8


data = bytes([0, 1, 2, 3, 4, 5 ])
# data = bytes([0, 1, 1,0,1,0,1,0 ])
print(data)
# print(int(data))
expected_checksum = 0xBC
crc_calculator = CrcCalculator(Crc8.CCITT)

checksum = crc_calculator.calculate_checksum(data)

print( checksum == expected_checksum)
print(hex(checksum).upper())
print(crc_calculator.verify_checksum(data, expected_checksum))
        
        # return False