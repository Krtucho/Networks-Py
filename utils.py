class Utils:
    @staticmethod
    def parse_hex_value(hex:str)->str: # hex variable must have this format: A5B4
        """Convierte un texto en hexadecimal de este formato:\nhex = 'A5B4'\nA este formato:hex = '0xffa'\n"""
        return f"0x{hex.lower()}" # hex variable will return with this format hex = '0xffa'
    
    @staticmethod
    def hex_to_dec(hex:str)->int:
        """Convierte un texto en hexadecimal a un numero entero"""
        # hex variable must have this format hex = '0xffa'
        return int(hex,16)
    
    @staticmethod
    def bin_to_hex(bin)->str: 
        """Convierte un numero binario en hexadecimal. bin puede ser un numero o string"""
        
        if isinstance(bin, str):
            bin = int(bin)
        dic_bin_hex  = {'0000': '0', '0001': '1', '0010': '2', '0011': '3', '0100': '4', '0101': '5',
            '0110': '6', '0111': '7', '1000': '8', '1001': '9', '1010': 'A', '1011': 'B',
            '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'}
        hex = ""
        i = 0
        while i <= len(bin)-4:
            b = ""
            for j in range(4):
                b = b+bin[i+j]
            hex = hex + dic_bin_hex[b]
            i = i+4
        return hex
    
    @staticmethod
    def hex_to_bin(hex:str)->int:
        """Convierte un numero hexadecimal en binario"""
        dic_hex_bin={'0':'0000','1':'0001','2':'0010','3':'0011','4':'0100','5':'0101',
        '6':'0110','7':'0111','8':'1000','9':'1001','A':'1010','B':'1011',
        'C':'1100','D':'1101','E':'1110','F':'1111'}
        bin=[]
        for i in hex:
            bin.append(dic_hex_bin[i])
        output = "".join(bin)
        return output