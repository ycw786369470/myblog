# def haft_find(l,r,list,num = 6):
#     if l <= r:
#         mid = (l + r) // 2
#         if num > list[mid]: # 如果num在中值右边
#             return haft_find(mid + 1, r, list)
#         elif num < list[mid]:
#             return haft_find(l, mid - 1, list)
#         else:
#             return mid
#
# if __name__ == '__main__':

#     index = haft_find(0, len(list1)-1, list1, 6)
#     print(index)



# list1 = []
# for i in range(11):
#     list1.append(i)
#
# l = 0
# r = 10
# num = 6
# while l <= r:
#     mid = (l + r)//2
#     if num > list1[mid]:
#         l = mid + 1
#     elif num < list1[mid]:
#         r = mid - 1
#     else:
#         print(mid)
#         break

# s = '1234'
# for item in s:
#     if item < '0' or item >'9':
#         print('no')
#         break
# else:
#     print('yes')
#
# for item in s:
#     if ord(item) < 48 or ord(item) > 57:
#         print('no')
#         break
# else:
#     print('yes')
#


# import math
# # x^2 + y^2 = r^2
# r = int(input('>>>'))
# x = -r
# while x<=1:
#     fx = (r**2 - x**2) ** 0.5
#     x += 0.05
#     画线(x,fx)


















import random
def random_num(n):
    num = ''
    for i in range(n):
        i = random.randint(0,9)
        num += str(i)
    print(num)

# random_num(3)





# l1 = 10**6
# r1 = 14.3
# r2 = 410**2
#
# a = (50.93*l1) / (r1*200*r2)
# a1 = (87.31*l1) / (r1*1040*r2)
# b = (111.12*l1) / (r1*1040*(385**2))
# b1 = (75.07*l1) / (r1*1040*r2)
# c = (85.8*l1) / (r1*200*r2)
import math
# ls1 = [a, a1, b, b1, c]
# for i in ls1:
#     n = 1-math.sqrt(1-2*i)
#     print(round(n,3))

# print("A为:"+str(round(a,3))+"\t1为:"+str(round(a1,3))+"\tB为:"+str(round(b,3))+'\t2为:'+str(round(b1,3))+'\tC为:'+str(round(c,3)))




# for i in range(0,100):
    # num = eval(input('请啾咪输入上面左边的值得数据>>>'))
    # down1 = eval(input('请啾咪输入下边是2300或者300'))
    # down2 = eval(input('请啾咪输入下边是610平方还是570平方'))
    #
    # n = (num*(10**6)) / (14.3*down1*(down2**2))
    # print(round(n,3))


ls = [0.037, 0.313, 0.021, 0.071]
l = []
for i in ls:
    n = (1 + math.sqrt(1 - 2*i)) / 2
    # print(round(n,3))
    l.append(round(n,3))
a = (446.75*(10**6))/(l[0]*360*571)
b = (436*(10**6))/(l[1]*360*570)
c = (259.77*(10**6))/(l[2]*360*610)
d = (112.92*(10**6))/(l[3]*360*610)
# print(l)
print(round(a,3))
print(round(b,3))
print(round(c,3))
print(round(d,4))



# n = 360
# a = (0.112*200*410*14.3)/n
# b = (0.036*1040*410*14.3)/n
# c = (0.052*200*385*14.3)/n
# d = (0.030*1040*410*14.3)/n
# e = (0.198*200*410*14.3)/n
# print(round(a,3),round(b,3),round(c,3),round(d,3),round(e,3))







