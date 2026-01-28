from space_network import *

class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet):
        print(f"[{self.name}] Received: {packet}")

sn = SpaceNetwork(level=1)
sat1 = Satellite("sat1", 100)
sat2 = Satellite("sat2", 200)
packet = Packet("Hi", sat1, sat2)

def main():
    sn.send(packet)

if __name__ == "__main__":
    main()