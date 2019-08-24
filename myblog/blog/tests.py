from django.test import TestCase

# Create your tests here.

#
# def f(x, ls=[]):
#     for i in range(x):
#         ls.append(i * i)
#     print(ls)
#
#
# f(3, [3, 2, 1])


# f = lambda a, b: a*b


# list = [1, 1, 3, 3, 5, 8]
# num = {}
# for i in list:
#     num[i] = num.get(i, 0) + 1
# print(num)

# ls = [1, 1, [1, 2, 3], [1, 2, [6]], 5, 8]
#
#
# def traverse(ls):
#     for i in ls:
#         if type(i) is list:
#             traverse(i)
#         else:
#             print(i)
#
# traverse(ls)


# def f():
#     return [lambda x: i+x for i in range(4)]
#
#
# # print(f())
# print([n(5) for n in f()])


# def f(ls1, ls2):
#     same_element = []
#     unsame_element = []
#     for i in ls1:
#         if i in ls2:
#             same_element.append(i)
#         else:
#             unsame_element.append(i)
#     for i in ls2:
#         if i not in ls1:
#             unsame_element.append(i)
#     return same_element, unsame_element


# ls1 = [1, 2, 3, 4]
# ls2 = [3, 4, 5, 7]
# # 1
# key1 = ls = ls1 + ls2
# # 2
# for i in ls2:
#     ls1.append(i)
# print(ls1)


# d = {'k': 1, 'v': 2}
# print(d.items())


# nums = []
# for i in range(10, 100):
#     nums.append(i if i%3 == 0 else 0)
# print(sum(nums))


# r = range(1,10)
# for i in r:
#     ls = []
#     for j in r:
#         ls.append(i * j)
#     print(ls)


# str = 'qwer'
# new_str = ''.join([str[i] for i in range(len(str) - 1, -1, -1)])
# print(new_str)

#
# str = "k:1|k1:2|k2:3|k3:4"
# str = str.split('|')
# d = {}
# for i in str:
#     s = i.split(':')
#     d[s[0]] = s[1]
# print(d)


list = [2, 4, 6, 8, 10]
i = 5
for j in range(len(list)):
    if list[j] > i:
        list.insert(j, i)
        break
print(list)