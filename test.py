def lru_cache(i):
    def greeting_decorator(func):
        def function_wrapper(x):
            if func.__name__=="get":
                for u in range(len(cache)):
                    if cache[u]["key"]==x:
                        print(cache[u]["data"])
                cache.append({"key":x,"data":func(x)})
                if len(cache)>i:
                    cache.pop(0)
            elif func.__name__=="put":
                cache.append({"key":func(x),"data":x})
                if len(cache)>i:
                    cache.pop(0)
            elif func.__name__=="delete":
                for u in range(len(cache)):
                    if cache[u]["key"]==x:
                        cache.pop(u)
                func(x)
        return function_wrapper
    return greeting_decorator

@lru_cache(5)
def foo(x):
    print(42)

foo("Hi")