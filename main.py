from space_network_lib import *
import time
from collections import deque

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
earth = Satellite("earth", 0)
sat1 = Satellite("sat1", 100)
sat2 = Satellite("sat2", 200)
sat3 = Satellite("sat3", 300)
sat4 = Satellite("sat4", 400)
packet = Packet("Hello from earth", sat3, sat4)
relay1 = RelayPacket(packet, sat2, sat3)
relay2 = RelayPacket(relay1, sat1, sat2)
relay3 = RelayPacket(relay2, earth, sat1)
p_final = Packet("Hello from earth", sat1, sat4)
p_earth_to_sat1 = RelayPacket(p_final, earth, sat1)
locations = {"earth": 0, "sat1": 100, "sat2": 200, "sat3": 300, "sat4": 400}

def find_path(entities, start, end):
    queue = deque([[start]])
    visited = {start}
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == end:
            return path
            
        for entity in entities:
            if entity not in visited and abs(node.distance_from_earth - entity.distance_from_earth) <= 150:
                visited.add(entity)
                queue.append(path + [entity])
    return None

def smart_send_packet(entities, initial_packet):
    path = find_path(entities, initial_packet.sender, initial_packet.receiver)
    
    if not path:
        print("No route found!")
        return

    print(f"Path found: {' -> '.join([e.name for e in path])}")
    current_packet = Packet(initial_packet.data, path[-2], path[-1])
    
    for i in range(len(path) - 3, -1, -1):
        current_packet = RelayPacket(current_packet, path[i], path[i+1])
    
    transmission_attempt(current_packet)

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
    all_entities = [earth, sat1, sat2, sat3, sat4]
    p_request = Packet("Hello From Earth!", earth, sat4)
    
    try:
        smart_send_packet(all_entities, p_request)
    except BrokenConnectionError:
        print("Transmission failed")

if __name__ == "__main__":
    main()