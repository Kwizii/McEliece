import random

from ecc import ECC
from util import *


# 创建私钥/公钥
def genKey(ecc: ECC):
    S = randInvMatrix(ecc.k)
    P = randPerMatrix(ecc.n)
    pub_key = (S@ecc.G@P)%2
    pv_key = (S, ecc.G, P)
    return pv_key, pub_key


class McEliece():
    def __init__(self, ecc: ECC, private_key, public_key):
        self.ecc = ecc
        if private_key is not None:
            S, G, P = private_key
            self.S, self.G, self.P, self.S_inv, self.P_inv = S, G, P, np.linalg.inv(S).astype(int), np.linalg.inv(
                P).astype(int)
        if public_key is not None:
            self.pub_key = public_key

    # 随机生成具有随机个1的错误码e，weight(e)<=t
    def random_error_code(self):
        # 生成一个长度为n的全0列表
        e = np.zeros(self.ecc.n, dtype=int)
        idx = random.randint(0, self.ecc.n - 1)
        e[idx] = 1
        return e

    # 加密
    def encrypt(self, m):
        assert self.pub_key is not None, '没有选择公钥'
        assert len(m) == self.ecc.k, '明文长度不正确'
        m = np.array(m, dtype=int)
        # 生成随机错误码
        e = self.random_error_code()
        # 明文m乘公钥得到密文
        encrypted = ((m@self.pub_key)%2 + e)%2
        return encrypted

    # 解密
    def decrypt(self, c):
        assert self.S is not None, '没有选择私钥'
        assert len(c) == self.ecc.n, '密文长度不正确'
        c = np.array(c, dtype=int)
        # 密文c乘P逆得到c_hat
        c_hat = (c@self.P_inv)%2
        # 对c_hat进行纠错
        c_hat = self.ecc.correct(c_hat)
        # 对c_hat进行解码得到m_hat
        m_hat = self.ecc.decode(c_hat)
        # m_hat乘S逆得到明文
        decrypted = (m_hat@self.S_inv)%2
        return decrypted

    # 加密字符串
    def encrypt_str(self, m: str):
        # 将明文字符串转为二进制串
        s = str2bin(m, self.ecc.k)
        # 将二进制串分组为长为k的二进制串
        rows = bin2vec(s, self.ecc.k)
        encrypted_bin = ''
        # 对每一组二进制串进行加密
        for row in rows:
            encrypted_bin += vec2bin([self.encrypt(row)])
        return encrypted_bin

    # 解密字符串
    def decrypt_str(self, c: str):
        # 将二进制串分组为长为n的二进制串
        rows = bin2vec(c, self.ecc.n)
        decrypted_bin = ''
        # 为每一组二进制串进行解密
        for row in rows:
            decrypted_bin += vec2bin([self.decrypt(row)])
        return bin2str(decrypted_bin)
