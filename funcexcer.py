def add(a, b):
     return a + b
def curried_add(a):
    def sec_arg(b):
        return a + b
    return sec_arg

print(curried_add(10)(20))
