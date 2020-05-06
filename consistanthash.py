import hashlib

from server_config import NODES

class Consistent_Node():
    def __init__(self, nodes):
        assert len(nodes) > 0
        self.nodes = nodes        


    def get_node(self, key_hex):
        key = int(key_hex, 16) # get the number from hex code
        node_index = key%(2**32) # get unique index from 0- 2^32 of a ring
        biggerrange = [] 
        subrange = []
        
        # to divide the circle into equally different part
        for i in range(len(self.nodes)):
            biggerrange.append(2**32-(((2**32)/len(self.nodes))*i))
        
        # becasue the node will choose the server depends on clockwise direction,
        # the node will choose the next closet server which is also the next larger node
        index = len(self.nodes)-1
        for i in range(len(self.nodes)):
            if node_index > biggerrange[i]:
                index = i-1
            elif node_index == biggerrange[i]:
                index = i


        # To divide again, this part is the virtual node layer
        for j in range(len(self.nodes)):
            subrange.append(biggerrange[index]-(biggerrange[index]/len(self.nodes)*j))
        
        index = len(self.nodes)-1
        for i in range(len(self.nodes)):
            if node_index > subrange[i]:
                index = i-1
            elif node_index == subrange[i]:
                index = i
        
        node_index=index
        return self.nodes[node_index]


def test():
    ring = Consistent_Node(nodes=NODES)
    node = ring.get_node('9ad5794ec94345c4873c4e591788743a')
    print(node)
    #print(ring.get_node('ed9440c442632621b608521b3f2650b8'))

#test()