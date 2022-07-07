class Route:
    def __init__(self, destination=[], mask=[], gateway=[], interface=0):
        self.destination = destination
        self.mask = mask
        self.gateway = gateway
        self.interface = interface

        