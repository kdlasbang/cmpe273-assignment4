import hashlib

from server_config import NODES

class Rendezvous_node():

    def __init__(self, nodes):
        assert len(nodes) > 0
        self.nodes = nodes
    
    def get_node(self, key_hex):
        weight=[]
        # below is the hash function to get weight(node,key)
        for i in range(len(self.nodes)):
            key = int(key_hex, 16)
            ss=str(self.nodes[i]['host'])+":"+str(self.nodes[i]['port'])
            a =int(hashlib.md5(ss.encode('utf-8')).hexdigest(), 16)
            weight.append(a%key)
        return self.nodes[weight.index(max(weight))]#get the max one


def test():
    ring = Rendezvous_node(nodes=NODES)
    node = ring.get_node('ed9440c442632621b608521b3f2650b8')
    print(node)
    #print(ring.get_node('ed9440c442632621b608521b3f2650b8'))


# Uncomment to run the above local test via: python3 node_ring.py
#test()
