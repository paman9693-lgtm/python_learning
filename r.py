# l = [1,2,3,4,5,6,7,8,9,10]
# def even_no(n):
#     if n%2==0:
#         return n
# res = list(filter(even_no,l))
# print(res)


# l = [1,2,3,4,5,6,7,8,9,10]
# def odd_no(n):
#     if n%2!=0:
#         return n
# res = list(filter(odd_no,l))
# print(res)


# l = [1,2,3,4,5,6,7,8,9,10]
# def greater_five(n):
#     if n>5:
#         return n
# res = list(filter(greater_five,l))
# print(res)


# l = [1,2,3,4,5,6,7,8,9,10]
# def less_than_five(n):
#     if n<5:
#         return n
# res = list(filter(less_than_five,l))
# print(res)


# import functools

# l=[1,2,3,4,5,6,7,8,9,]
# def even_no_sum(n1,n2):
#     if n1%2==0 and n2%2==0:
#         return n1+n2
#     elif n1%2==0:
#         return n1
#     elif n2%2==0:
#         return n2
# res = functools.reduce(even_no_sum,l)
# print(res)



# import functools

# l=[0]
# def even_no_sum(n1,n2):
#     if n1%2==0 and n2%2==0:
#         return n1+n2
#     elif n1%2==0:
#         return n1
#     elif n2%2==0:
#         return 0
# res = functools.reduce(even_no_sum,l)
# print(res)



import functools

l = [0,1, 2, 3, 4, 5, 6, 7, 8, 9]

def odd_no_sum(n1, n2):
    if n2 % 2 != 0:
        n1=n1+n2
        return n1
    else:
        return n1
    
res = functools.reduce(odd_no_sum, l)
print(res)

import functools

l = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def even_no_sum(n1, n2):
    if n2 % 2 == 0:
        n1=n1+n2
        return n1
    else:
        return n1
res = functools.reduce(even_no_sum, l,0)
print(res)