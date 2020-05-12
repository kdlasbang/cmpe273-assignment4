import sys
import socket
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from node_ring import NodeRing
from rendezvousHash import Rendezvous_node
from consistanthash import Consistent_Node
from lru_cache import lru_cache
from bloom_filter import BloomFilter 


NUM_KEYS = 20 
FALSE_POSITIVE_PROBABILITY = 0.05
bloomfilter = BloomFilter(NUM_KEYS, FALSE_POSITIVE_PROBABILITY) 
BUFFER_SIZE = 1024
globalclient=[]

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()

# value and key need to be after serialize
def put(key,value):
    global globalclient
    ring = NodeRing(nodes=NODES)
    node = ring.get_node(key)
    fix_me_server_id = node['port']-4000
    #fix_me_server_id=0
    response = globalclient[fix_me_server_id].send(value)
    bloomfilter.add(response)
    return response

@lru_cache(5)
def get(hc):
    global globalclient
    if bloomfilter.is_member(hc):
        data_bytes, key = serialize_GET(hc)
        ring = NodeRing(nodes=NODES)
        node = ring.get_node(key)
        fix_me_server_id = node['port']-4000
        #fix_me_server_id=0
        response = globalclient[fix_me_server_id].send(data_bytes)
        return response
    else:
        return None

def delete(hc):
    global globalclient
    if bloomfilter.is_member(hc):
        data_bytes, key = serialize_DELETE(hc)
        ring = NodeRing(nodes=NODES)
        node = ring.get_node(key)
        fix_me_server_id = node['port']-4000
        #fix_me_server_id=0
        response = globalclient[fix_me_server_id].send(data_bytes)
        return response
    else:
        return None



def process(udp_clients):
    hash_codes = set()
    global globalclient
    globalclient = udp_clients
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        response = put(key,data_bytes)
        print(response)
        hash_codes.add(response)
    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    

    # TODO: PART I
    # GET all users.
    for hc in hash_codes:
        print(hc)
        response = get(hc)
        print(response)

    #delete all users
    htest=hash_codes.copy()
    for hc in htest:
        print(hc)
        response = delete(hc)
        print(response)
        hash_codes.remove(hc)
    #print(hash_codes)


if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)

