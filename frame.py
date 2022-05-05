class Frame:
    def __init__(self, state="active", src_mac="", dst_mac="", size=0)-> None:
        self.state = state
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.size = size
        