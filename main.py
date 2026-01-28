from space_network import *
import time

class Satellite(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet):
        print(f"[{self.name}] Received: {packet}")

class BrokenConnectionError(Exception):
    pass

sn = SpaceNetwork(level=3)
sat1 = Satellite("sat1", 100)
sat2 = Satellite("sat2", 200)
packet = Packet("Hi", sat1, sat2)

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
    try:
        transmission_attempt(packet)
    except BrokenConnectionError:
        print("Transmission failed")

if __name__ == "__main__":
    main()