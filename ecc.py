from abc import ABC, abstractmethod


# 纠错码抽象类定义
class ECC(ABC):
    # 数据长度
    @property
    @abstractmethod
    def k(self):
        pass

    # 编码长度
    @property
    @abstractmethod
    def n(self):
        pass

    # 纠错能力
    @property
    @abstractmethod
    def t(self):
        pass

    # 生成矩阵G
    @property
    @abstractmethod
    def G(self):
        pass

    # 纠错矩阵H
    @property
    @abstractmethod
    def H(self):
        pass

    # 编码
    @abstractmethod
    def encode(self, m):
        pass

    # 解码
    @abstractmethod
    def decode(self, c):
        pass

    # 纠错
    @abstractmethod
    def correct(self, c):
        pass
