import hashlib

from server_config import NODES

class NodeRing():

    def __init__(self, nodes):
        assert len(nodes) > 0
        self.nodes = nodes
    
    def get_node(self, key_hex):
        key = int(key_hex, 16)
        weight=[]
        # below is the hash function to get weight(node,key)
        for i in range(len(self.nodes)):
            ss=str(self.nodes[i]['host'])+":"+str(self.nodes[i]['port'])
            a=hash(ss)%(2**32)
            weight.append(key%a)
        # from the list get the max weight(node, key) and return 
        return self.nodes[weight.index(max(weight))]


def test():
    ring = NodeRing(nodes=NODES)
    node = ring.get_node('9ad5794ec94345c4873c4e591788743a')
    print(node)
    #print(ring.get_node('ed9440c442632621b608521b3f2650b8'))


# Uncomment to run the above local test via: python3 node_ring.py
#test()
