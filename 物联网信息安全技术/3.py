import random

# ==========================================
# 1. 扩展欧几里得算法与求逆算法
# ==========================================
def ext_gcd(a, b):
    """
    扩展欧几里得算法
    返回 (x, y, gcd) 使得 a*x + b*y = gcd(a, b)
    """
    if b == 0:
        return 1, 0, a
    else:
        x, y, gcd = ext_gcd(b, a % b)
        # 递推更新 x, y
        x, y = y, (x - (a // b) * y)
        return x, y, gcd

def mod_inverse(a, m):
    """
    求 a 在模 m 下的乘法逆元
    即求 x 使得 a*x ≡ 1 (mod m)
    """
    x, y, gcd = ext_gcd(a, m)
    if gcd != 1:
        return None # 不存在逆元
    else:
        return x % m

# ==========================================
# 2. 随机素数生成相关函数
# ==========================================
def is_prime(num):
    """简单的素数判断函数"""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime(min_val, max_val):
    """在指定范围内随机生成一个素数"""
    while True:
        num = random.randint(min_val, max_val)
        if is_prime(num):
            return num

# ==========================================
# 3. RSA 密钥生成、加密与解密
# ==========================================
def generate_keys():
    """生成 RSA 公钥和私钥"""
    # 1. 随机生成两个不同的素数 p 和 q (这里为了演示选取较小的素数区间)
    p = generate_prime(100, 500)
    q = generate_prime(100, 500)
    while p == q:
        q = generate_prime(100, 500)
        
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    # 2. 私有密钥 d 随机产生，要求 gcd(d, phi_n) == 1
    d = random.randint(2, phi_n - 1)
    while True:
        # 检查是否互素
        _, _, gcd_val = ext_gcd(d, phi_n)
        if gcd_val == 1:
            break
        d = random.randint(2, phi_n - 1)
        
    # 3. 公开密钥 e 利用求逆算法给出 (e 是 d 模 phi_n 的逆元)
    e = mod_inverse(d, phi_n)
    
    return (e, n), (d, n)

def encrypt(plaintext, public_key):
    """加密过程：明文 -> 密文"""
    e, n = public_key
    # 将输入的字符串每个字符转为 ASCII，然后应用公式 (M^e) mod n
    cipher = [(ord(char) ** e) % n for char in plaintext]
    return cipher

def decrypt(ciphertext, private_key):
    """解密过程：密文 -> 明文"""
    d, n = private_key
    # 应用公式 (C^d) mod n，然后将 ASCII 码转回字符
    plain = [chr((char ** d) % n) for char in ciphertext]
    return ''.join(plain)

# ==========================================
# 4. 主程序交互流程
# ==========================================
if __name__ == '__main__':
    print("=== RSA 加密解密演示系统 ===")
    
    # 自动生成密钥对
    print("\n[系统] 正在生成密钥对...")
    public_key, private_key = generate_keys()
    print(f"随机生成的私钥 (d, n): {private_key}")
    print(f"通过求逆算法计算的公钥 (e, n): {public_key}")
    
    # --- 加密阶段 ---
    print("\n--- 加密过程 ---")
    message = input("请输入需要加密的明文: ")
    encrypted_msg = encrypt(message, public_key)
    print(f"加密后的密文 (数组形式): {encrypted_msg}")
    
    # --- 解密阶段 ---
    print("\n--- 解密过程 ---")
    # 为了模拟键盘输入密文和私钥，我们将之前的输���转换为字符串提示用户输入
    input_cipher_str = input("请输入密文 (以逗号分隔的数字，例如 123,456): ")
    input_d = int(input("请输入私钥 d: "))
    input_n = int(input("请输入模数 n: "))
    
    # 处理输入的密文
    try:
        input_cipher = [int(x.strip()) for x in input_cipher_str.split(',')]
        user_private_key = (input_d, input_n)
        
        decrypted_msg = decrypt(input_cipher, user_private_key)
        print(f"\n[成功] 解密算法输出的明文: {decrypted_msg}")
    except Exception as err:
        print(f"\n[错误] 输入格式有误或解密失败: {err}")