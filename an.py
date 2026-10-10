# l=[1,2,3,4,8,5,654]
# def even_no(n):
#     if n%2==0:
#         return n
# result=list(filter(even_no,l))
# print(result)
# print(tuple(result))


# l=[1,2,3,4,8,5,654]
# def odd_no(n):
#     if n%2!=0:
#         return n
# result=list(filter(odd_no,l))
# print(result)
# print(tuple(result))



# l=[1,2,3,4,8,5,654]
# def greater_five(n):
#     if n>5:
#         return n
# result=list(filter(greater_five,l))
# print(result)
# print(tuple(result))



# l=[1,2,3,4,8,5,654]
# def less_than_five(n):
#     if n<5:
#         return n
# result=list(filter(less_than_five,l))
# print(result)
# print(tuple(result))     



# #out put
# [2, 4, 8, 654]
# (2, 4, 8, 654)
# [1, 3, 5]
# (1, 3, 5)
# [8, 654]
# (8, 654)
# [1, 2, 3, 4]
# (1, 2, 3, 4)



import functools


functools


# l=[1,2,3,4,5,6,7,8,9,10]
# def max_no(n1,n2):
#     if n1 > n2:
#         return n1
#     else:
#         return n2
# res= functools.reduce(max_no,l)
# print(res)
# out put
# 10




# l=[1,2,3,4,5,6,7,8,9,10]
# def max_no(n1,n2):
#     if n1 <n2:
#         return n1
#     else:
#         return n2
# res= functools.reduce(max_no,l)
# print(res)
# out_put
# 1



# Total of all numbers using functools.reduce
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# def total_sum(n1, n2):
#     return n1 + n2

# result = functools.reduce(total_sum, numbers)
# print(result)
# output
# 55


import functools

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

total = functools.reduce(lambda a, b: a + b, numbers)
average = total / len(numbers)

print("Total:", total)
print("Average:", average)