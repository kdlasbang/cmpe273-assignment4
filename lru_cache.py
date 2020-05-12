cache=[]

def saveCache(cache):
    with open('LRUCacheHistory.txt', 'w') as f:
        for item in cache:
            f.write("%s\n" % item)

def lru_cache(i):
    def greeting_decorator(func):
        def function_wrapper(x):
            for u in range(len(cache)):
                if cache[u]["key"]==x:
                    #print("[cache-hit]--",x,cache[u]["data"])
                    return (cache[u]["data"])
            output = func(x)
            cache.append({"key":x,"data":output})
            if len(cache)>i:
                cache.pop(0)
            saveCache(cache)
            return output
        return function_wrapper
    return greeting_decorator