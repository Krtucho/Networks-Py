from frame import Frame

class PortData:
    def __init__(self, ip="", mac=""):
        self.ip = ip
        self.mac = mac
        
        # Frames que estan entrando, es decir, que el router recibe
        self.in_frames = []
        self.in_frame_index = -1

        # Frames que estan saliendo, es decir q el router envia
        self.out_frames = []
        self.out_frame_index = -1
        
    def add_frame_in(self, frame):
        if len(self.in_frames) == 0:
            self.in_frame_index = 0
        self.in_frames.append(frame)
        
    def add_frame_out(self, frame):
        if len(self.out_frames) == 0:
            self.out_frame_index = 0
        self.out_frames.append(frame)
        
    def set_ip(self, ip):
        self.ip = ip
        
    def set_mac(self, mac):
        self.mac = mac