from hamming import Hamming
from mceliece import McEliece, genKey

if __name__ == '__main__':
    # 选择纠错码
    h = Hamming(15)  # h = Goppa()
    # 根据纠错码生成密钥对
    pvKey, pubKey = genKey(h)
    print(f'私钥S：\n{pvKey[0]}\n私钥P：\n{pvKey[2]}')
    print(f'公钥G_hat：\n{pubKey}')
    mceliece = McEliece(h, pvKey, pubKey)
    # 选择明文
    m = "~~~~你好，世界~~~~"
    print('明文', m)
    # 通过公钥对明文进行加密
    c = mceliece.encrypt_str(m)
    # 以十六进制显示密文
    print('密文', hex(int(c, 2)))
    # 通过私钥
    mm = mceliece.decrypt_str(c)
    print('解密', mm)
    pass
