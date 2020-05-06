import hashlib
from server_config import NODES

def add_server_node( key, rangeList):
    rangeList.append(key)

def remove_server_node(key, rangeList ):
    rangeList.remove(key)

def get_range(key, rangeList):
    rangeList.sort()
    for i in range(len(rangeList)):
        if key > rangeList[i]:
            continue
        else:
            return i
    return 0



class Consistent_Node():
    def __init__(self, nodes):
        assert len(nodes) > 0
        self.nodes = nodes        


    def get_node(self, key_hex):
        key = int(key_hex, 16) # get the number from hex code
        node_index = key%(2**32) # get unique index from 0- 2^32 of a ring
        biggerrange = [] 
        subrange = []
        nodeDict=[]
        
        # hash the server node and put into the ring
        for i in range(len(self.nodes)):
            ss=str(self.nodes[i]['host'])+":"+str(self.nodes[i]['port'])
            kk= int(hashlib.md5(ss.encode('utf-8')).hexdigest(), 16)
            vk= int(hashlib.sha256(ss.encode('utf-8')).hexdigest(), 16) #generate virtual node
            server_key= kk%(2**32)
            virtual_server_key = vk%(2**32)
            nodeDict.append({'key' : virtual_server_key, 'index':i})
            nodeDict.append({'key' : server_key, 'index':i})
            add_server_node( server_key, biggerrange)
            add_server_node(virtual_server_key,biggerrange)
        
        # because the node will choose the server depends on clockwise direction,
        # the node will choose the next closet server which is also the next larger node
        rangeArea = get_range(node_index, biggerrange)
        for i in range(len(nodeDict)):
            if nodeDict[i]['key']==biggerrange[rangeArea]:
                return self.nodes[nodeDict[i]['index']]
        node_index=0
        return self.nodes[node_index]


def test():
    ring = Consistent_Node(nodes=NODES)
    node = ring.get_node('9ad5794ec94345c4873c4e591788743a')
    print(node)
    #print(ring.get_node('ed9440c442632621b608521b3f2650b8'))

#test()