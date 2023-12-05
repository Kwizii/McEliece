import numpy as np

from ecc import ECC


class Hamming(ECC):
    def __init__(self, k=4):
        assert k > 0, '编码的数据长度要大于0'
        self.k_ = k
        r = 1
        while 2 ** r - r - 1 < k:
            r += 1
        self.r_ = r
        print(f'Hamming({self.n},{self.k},{self.r})')
        # 生成每列是索引对应二进制的矩阵
        bin_matrix = np.array([[((j + 1)//(2 ** i))%2 for j in range(2 ** r - 1)] for i in range(r)], dtype=int)
        # 去掉校验位
        check_cols = []
        for i in range(r):
            check_cols.append(2 ** i - 1)
        bin_matrix = np.delete(bin_matrix, check_cols, axis=1)
        # 保留数据长度k
        control_matrix = bin_matrix[:, :k]
        # 创建纠错矩阵
        self.H_ = np.hstack((control_matrix, np.eye(r))).astype(int)
        # 创建生成矩阵
        self.G_ = np.hstack((np.eye(k), control_matrix.T)).astype(int)

    # 数据长度
    @property
    def k(self):
        return self.k_

    # 码字长度
    @property
    def n(self):
        return self.k + self.r

    # 校验位长度
    @property
    def r(self):
        return self.r_

    # 纠错能力
    @property
    def t(self):
        return 1

    # 海明码生成矩阵
    @property
    def G(self):
        return self.G_

    # 海明码纠错矩阵
    @property
    def H(self):
        return self.H_

    # 将消息m编码为码字
    def encode(self, m):
        return m@self.G

    # 将码字c解码为消息
    def decode(self, c):
        return c[:self.k]

    # 对码字c进行纠错(至多1位)
    def correct(self, c):
        syndrome = (self.H@c.T)%2
        for idx, col in enumerate(self.H.T):
            if np.all(col == syndrome):
                c[idx] ^= 1
                break
        return c
