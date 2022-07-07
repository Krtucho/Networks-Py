from frame import Frame

class PortData:
    def __init__(self, ip="", mac="", mask=""):
        self.ip = ip
        self.mac = mac
        self.mask = mask
        
        # Frames que estan entrando, es decir, que el router recibe
        self.in_frames = []
        self.in_frame_index = -1

        # Frames que estan saliendo, es decir q el router envia
        self.out_frames = []
        self.out_frame_index = -1
        self.last_updated_frame_time = 0 # Tiempo transcurrido desde que se envio el ultimo bit
        
        self.pending = False
        self.sending = False
        self.transmitting = False
        self.waiting = False
        
    def add_frame_in(self, frame):
        if len(self.in_frames) == 0:
            self.in_frame_index = 0
        self.in_frames.append(frame)
        
    def add_frame_out(self, frame):
        if len(self.out_frames) == 0:
            self.out_frame_index = 0
        self.out_frames.append(frame)
        
    def set_ip(self, ip, mask):
        self.ip = ip
        self.mask = mask
        
    def set_mac(self, mac):
        self.mac = mac
        
    def update_bit_time(self, ms: int, collision: bool):
        if self.time_to_send_next_bit == 0:
            # Si aun faltan bits por enviar resetea el tiempo restante de envio y extrae el primer bit de la lista que fue la que se envio
            self.bits_to_send.pop(0) #  extrae el primer bit de la lista que fue la que se envio
            if len(self.bits_to_send) != 0: # Si solamente queda
                self.actual_bit = self.bits_to_send[0] # actualiza el bit que se esta enviando actualmente
                # self.write_msg_in_file(f"{ms} {self.port.name} send {self.actual_bit} {'collision' if collision else 'ok'}")
                self.time_to_send_next_bit = self.signal_time -1
            else:
                self.pending = False
                self.writing = False
                self.transmitting = False
                self.actual_bit = -1
                self.time_to_send_next_bit = self.signal_time -1
        elif self.time_to_send_next_bit > 0:
            self.time_to_send_next_bit -= 1