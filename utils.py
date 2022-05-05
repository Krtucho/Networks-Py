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
    def bin_to_hex(bin:int)->str:
        """Convierte un numero decimal en un texto en hexadecimal"""
        return ""
    
    @staticmethod
    def hex_to_bin(hex:str)->int:
        """Convierte un numero hexadecimal en binario"""
        return 0