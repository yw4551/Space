from space_network import *
import time

class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):
        super().__init__(packet_to_relay, sender, proxy)

    def __repr__(self):
        return f"RelayPocket(Relaying [{self.data}] to {self.receiver} from {self.sender})"

class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet):
        if isinstance(packet, RelayPacket):
            inner_pocket = packet.data
            print(f"Unwrapping and forwarding to {inner_pocket.receiver}")
            transmission_attempt(inner_pocket)
        else:
            print(f"Final destination reached: {packet.data}")

class BrokenConnectionError(Exception):
    pass

sn = SpaceNetwork(level=3)
sat1 = Satellite("sat1", 100)
sat2 = Satellite("sat2", 200)
earth = Satellite("earth", 0)
p_final = Packet("Hello from earth", sat1, sat2)
p_earth_to_sat1 = RelayPacket(p_final, earth, sat1)

def transmission_attempt(packet):
    while True:
        try:
            sn.send(packet)
        except TemporalInterferenceError:
            print("Interference waiting...")
            time.sleep(2)
            continue
        except DataCorruptedError:
            print("Data corrupted, retrying...")
            continue
        except LinkTerminatedError:
            print("Link lost")
            raise BrokenConnectionError("Link lost")
        except OutOfRangeError:
            print("Target out of range")
            raise BrokenConnectionError("Target out of range")
        break

def main():
    transmission_attempt(p_earth_to_sat1)

if __name__ == "__main__":
    main()