import binascii

import numpy as np


# 创建随机可逆矩阵
def randInvMatrix(r, c=None):
    if not c:
        c = r
    while True:
        # 创建随机稀疏可逆矩阵
        m = np.random.randint(0, 2, (r, c))
        if int(np.linalg.det(m)):
            # 找到的矩阵S须满足：S的逆矩阵在类型强转为int后仍为S的逆矩阵
            m = m.astype(int)
            m_inv = np.linalg.inv(m).astype(int)
            mul = m@m_inv
            if np.all(mul == np.eye(r, c, dtype=int)):
                break
    return m


# 创建随机置换矩阵
def randPerMatrix(n):
    p = np.random.permutation(n)
    m = np.zeros((n, n), dtype=int)
    for i in range(n):
        m[i, p[i]] = 1
    return m


# 字符串转二进制字符串
# k：用来将二进制长度对k取整
def str2bin(s, k):
    encoded = s.encode('utf8')
    bin_str = bin(int(binascii.hexlify(encoded), 16))[2:]
    if len(bin_str)%k:
        bin_str = bin_str.zfill(k*(len(bin_str)//k + 1))
    return bin_str


# 二进制串转字符串
def bin2str(s):
    return binascii.unhexlify(hex(int(s, 2))[2:]).decode('utf8')


# 将二进制串分组为每段长为n的向量组
def bin2vec(s, n):
    return np.array([np.array([int(bit) for bit in s[gp*n:(gp + 1)*n]], dtype=int).T for gp in range(len(s)//n)],
                    dtype=int)


# 将向量组转为二进制串
def vec2bin(vecs):
    bin_str = ''
    for vec in vecs:
        row_str = np.array_str(vec)
        bin_str += row_str.replace('[', '').replace(']', '').replace(' ', '')
    return bin_str
