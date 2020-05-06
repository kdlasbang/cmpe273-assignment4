import sys
import socket
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, serialize_DELETE
from node_ring import NodeRing

BUFFER_SIZE = 1024
hash_codes = set()
cache= []

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


def savefileBloomfilter(hash_codes):
    with open('bloomfilterMemberSet.py', 'w') as fp:
        fp.write(str(hash_codes))

def saveCache(cache):
    with open('LRUCache.py', 'w') as f:
        for item in cache:
            f.write("%s\n" % item)


def lru_cache(i):
    def greeting_decorator(func):
        def function_wrapper(x,y,z):
            if func.__name__=="get":
                for u in range(len(cache)):
                    if cache[u]["key"]==x:
                        return (cache[u]["data"])
                output = func(x,y,z)
                cache.append({"key":x,"data":output})
                if len(cache)>i:
                    cache.pop(0)
                saveCache(cache)
                return output
            elif func.__name__=="put":
                out= func(x,y,z)
                cache.append({"key":out,"data":y})
                if len(cache)>i:
                    cache.pop(0)
                saveCache(cache)
                return out
            elif func.__name__=="delete":
                for u in range(len(cache)):
                    if cache[u]["key"]==x:
                        cache.pop(u)
                        saveCache(cache)
                        return func(x,y,z)
        return function_wrapper
    return greeting_decorator

def bloomfilter_is_member(key):
    global hash_codes
    return key in hash_codes

def bloomfilter_add(key):
    global hash_codes
    hash_codes.add(key)
    savefileBloomfilter(hash_codes)

def bloomfilter_delete(key):
    global hash_codes
    hash_codes.remove(key)
    savefileBloomfilter(hash_codes)

# value and key need to be after serialize
@lru_cache(5)
def put(key,value,udp_clients):
    # TODO: PART II - Instead of going to server 0, use Naive hashing to split data into multiple servers
    ring = NodeRing(nodes=NODES)
    node = ring.get_node(key)
    fix_me_server_id = node['port']-4000
    #fix_me_server_id=0
    response = udp_clients[fix_me_server_id].send(value)
    bloomfilter_add(response)
    return response

@lru_cache(5)
def get(key, value , udp_clients):
    if bloomfilter_is_member(key):
        ring = NodeRing(nodes=NODES)
        node = ring.get_node(key)
        fix_me_server_id = node['port']-4000
        #fix_me_server_id=0
        response = udp_clients[fix_me_server_id].send(value)
        return response
    else:
        return None

@lru_cache(5)
def delete(key,value,udp_clients):
    if bloomfilter_is_member(key):
        ring = NodeRing(nodes=NODES)
        node = ring.get_node(key)
        fix_me_server_id = node['port']-4000
        #fix_me_server_id=0
        response = udp_clients[fix_me_server_id].send(value)
        bloomfilter_delete(key)
        return response
    else:
        return None



def process(udp_clients):
    global hash_codes
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        response = put(key,data_bytes,udp_clients)
        print(response)
    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")
    

    # TODO: PART I
    # GET all users.
    for hc in hash_codes:
        print(hc)
        data_bytes, key = serialize_GET(hc)
        response = get(key, data_bytes, udp_clients)
        print(response)
    
    htest=hash_codes.copy()
    for hc in htest:
        data_bytes, key = serialize_DELETE(hc)
        response = delete(key, data_bytes,udp_clients)
        print(response)
        


if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    process(clients)

