cache=[]
def lru_cache(i):
    def greeting_decorator(func):
        def function_wrapper(x,y,z):
            if func.__name__=="get":
                print("----")
                for u in range(len(cache)):
                    if cache[u]["key"]==x:
                        return (cache[u]["data"])
                cache.append({"key":x,"data":func(x,y,z)})
                if len(cache)>i:
                    cache.pop(0)
            elif func.__name__=="put":
                print("****")
                cache.append({"key":func(x,y,z),"data":y})
                if len(cache)>i:
                    cache.pop(0)
            elif func.__name__=="delete":
                print("++++")
                for u in range(len(cache)):
                    if cache[u]["key"]==x:
                        cache.pop(u)
                func(x,y,z)
        return function_wrapper
    return greeting_decorator

@lru_cache(5)
def put(key,value,udp_clients):
    return "put"

@lru_cache(5)
def get(key,value,udp_clients):
    return "get"

@lru_cache(5)
def delete(key,value,udp_clients):
    return "delete"

key="key"
value = "value"
udp_clients="udp_clients"
put(3,1,udp_clients)
for i in range (len(cache)):
    print(cache[i])
put(4,2,udp_clients)
for i in range (len(cache)):
    print(cache[i])
put(5,3,udp_clients)
for i in range (len(cache)):
    print(cache[i])
put(6,4,udp_clients)
for i in range (len(cache)):
    print(cache[i])
put(7,5,udp_clients)
for i in range (len(cache)):
    print(cache[i])
put(8,100,udp_clients)
for i in range (len(cache)):
    print(cache[i])
get(3,100,udp_clients)
for i in range (len(cache)):
    print(cache[i])