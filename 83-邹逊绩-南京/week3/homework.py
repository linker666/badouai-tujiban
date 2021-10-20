'''
作业：根据词典，输出一段文本所有可能的切割方式
'''
# coding:utf-8
import numpy as np
from collections import defaultdict

# 词典，每个词后方存储的是其词频，仅为示例，也可自行添加
Dict = {"经常": 0.1, "经": 0.05, "有": 0.1, "常": 0.001, "有意见": 0.1, "歧": 0.001, "意见": 0.2, "分歧": 0.2, "见": 0.05, "意": 0.05,
        "见分歧": 0.05, "分": 0.1}
dd = [(key) for key, _ in Dict.items()]
# print(dd)
content = "经常有意见分歧"
a = len(content) - 1
pp = []

for i in range(2 ** a):
    ss = np.binary_repr(i, width=a)

    total = 0
    pos = 1
    str = content[0]
    ll = []
    for ch in ss:
        if ch == '0':
            str = str + content[pos]
        else:
            if not (str in dd):
                continue
            ll.append(str)
            total = total + len(str)
            str = content[pos]

        pos = pos + 1

    if (str in dd):
        ll.append(str)
        total = total + len(str)

    if total == len(content):
        pp.append(ll)
        print(ll)

# 为什么只是一行, 不能象下面这样输出
print(pp)

"""
预期输出
[['经常', '有意见', '分歧'], 
 ['经常', '有意见', '分', '歧'],
 ['经常', '有', '意见', '分歧'], 
 ['经常', '有', '意见', '分', '歧'], 
 ['经常', '有', '意', '见分歧'], 
 ['经常', '有', '意', '见', '分歧'], 
 ['经常', '有', '意', '见', '分', '歧'], 
 ['经', '常', '有意见', '分歧'], 
 ['经', '常', '有意见', '分', '歧'], 
 ['经', '常', '有', '意见', '分歧'], 
 ['经', '常', '有', '意见', '分', '歧'], 
 ['经', '常', '有', '意', '见分歧'], 
 ['经', '常', '有', '意', '见', '分歧'], 
 ['经', '常', '有', '意', '见', '分', '歧']]
"""
