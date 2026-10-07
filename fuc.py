# 


def outer():
    x=10
    def inner():
        nonlocal x
        print(x)
        x=20
        return x
    res = inner()
    return res
result = outer()
print(result)