# 1. 扩展欧几里得算法与仿射密码
def extended_gcd(a, b):
    """
    扩展欧几里得算法
    返回 (gcd, x, y) 使得 a*x + b*y = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y
def mod_inverse(a, m):
    """求 a 模 m 的乘法逆元"""
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"密钥 a={a} 与 m={m} 不互素，不存在逆元！")
    return x % m
def affine_encrypt(plaintext, a, b):
    """仿射密码加密: E(x) = (a * x + b) mod 26"""
    ciphertext = ""
    for char in plaintext.upper():
        if char.isalpha():
            x = ord(char) - 65
            c = (a * x + b) % 26
            ciphertext += chr(c + 65)
        else:
            ciphertext += char
    return ciphertext
def affine_decrypt(ciphertext, a, b):
    """仿射密码解密: D(y) = a^-1 * (y - b) mod 26"""
    plaintext = ""
    a_inv = mod_inverse(a, 26) # 使用扩展欧几里得算法求逆元
    for char in ciphertext.upper():
        if char.isalpha():
            y = ord(char) - 65
            p = (a_inv * (y - b)) % 26
            plaintext += chr(p + 65)
        else:
            plaintext += char
    return plaintext
# 2. Playfair 密码
def generate_playfair_matrix(key):
    """生成 Playfair 5x5 密码矩阵 (将 J 视作 I)"""
    key = "".join([c.upper() for c in key if c.isalpha()]).replace("J", "I")
    matrix = []
    seen = set()
    # 填充密钥
    for char in key:
        if char not in seen:
            seen.add(char)
            matrix.append(char)
    # 填充剩余字母
    for i in range(26):
        char = chr(i + 65)
        if char == "J":
            continue
        if char not in seen:
            seen.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]
def find_position(matrix, char):
    """查找字符在矩阵中的行列索引"""
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return -1, -1
def playfair_process_text(text):
    """预处理 Playfair 明文:去除非字母,填充矩阵,J 转 I,相同字母插入 X,奇数长度补 X"""
    text = "".join([c.upper() for c in text if c.isalpha()]).replace("J", "I")
    processed = ""
    i = 0
    while i < len(text):
        char1 = text[i]
        if i + 1 < len(text):
            char2 = text[i+1]
            if char1 == char2:
                processed += char1 + "X"
                i += 1
            else:
                processed += char1 + char2
                i += 2
        else:
            processed += char1 + "X"
            i += 1
    return processed

def playfair_remove_padding_x(text):
    """移除 Playfair 解密中由规则引入的填充 X"""
    if not text:
        return text
    cleaned = []
    i = 0
    while i < len(text):
        # 形如 A X A 的模式中，X 通常是为拆分重复字母而插入的填充字符
        if i + 2 < len(text) and text[i] == text[i + 2] and text[i + 1] == "X":
            cleaned.append(text[i])
            cleaned.append(text[i + 2])
            i += 3
        else:
            cleaned.append(text[i])
            i += 1
    # 奇数长度补位的末尾 X
    if cleaned and cleaned[-1] == "X":
        cleaned.pop()
    return "".join(cleaned)
def playfair_cipher(text, key, mode="encrypt"):
    """Playfair 加密与解密核心逻辑"""
    matrix = generate_playfair_matrix(key)
    if mode == "encrypt":
        text = playfair_process_text(text)
        shift = 1
    else:
        # 解密时假设文本已经是偶数长度的合法密文
        shift = -1
    result = ""
    for i in range(0, len(text), 2):
        r1, c1 = find_position(matrix, text[i])
        r2, c2 = find_position(matrix, text[i+1])
        if r1 == r2: # 同行：右/左移
            result += matrix[r1][(c1 + shift) % 5]
            result += matrix[r2][(c2 + shift) % 5]
        elif c1 == c2: # 同列：下/上移
            result += matrix[(r1 + shift) % 5][c1]
            result += matrix[(r2 + shift) % 5][c2]
        else: # 矩形：交换列
            result += matrix[r1][c2]
            result += matrix[r2][c1]   
    if mode == "decrypt":
        return playfair_remove_padding_x(result)
    return result
# 3. 穷举搜索法破译移位密码
def brute_force_shift_cipher(ciphertext):
    """穷举破解移位加密，只输出符合英文语义的正确解密"""
    print(f"--- 穷举搜索法破译移位密码 ---")
    print(f"待破译密文: {ciphertext}")
    # 穷举所有可能的位移量 1-25
    for shift in range(1, 26):
        decrypted = ""
        for char in ciphertext:
            if char.isalpha():
                # 凯撒密码解密: D(x) = (x - shift) mod 26
                decrypted += chr((ord(char) - 65 - shift) % 26 + 65)
            else:
                decrypted += char               
        # 启发式识别：如果解密后的句子包含特定的常见单词或词根
        # 针对你提供的密文，我们使用常见词汇进行筛选匹配
        if "THE" in decrypted and ("IN" in decrypted or "OF" in decrypted or "TO" in decrypted):
            print(f"位移量: {shift}")
            print(f"正确明文: {decrypted}")
            return # 找到并输出后立即结束，不再输出错误的解密结果           
    print("未发现有意义的明文。")
# ================= 测试与执行 =================
if __name__ == "__main__":
    print("1. 仿射密码演示")
    # 选择 a=5, b=8 (5 和 26 互素)
    affine_a, affine_b = 5, 8
    test_text = "HELLOWORLD"
    enc_affine = affine_encrypt(test_text, affine_a, affine_b)
    dec_affine = affine_decrypt(enc_affine, affine_a, affine_b)
    print(f"明文: {test_text}")
    print(f"密钥: a={affine_a}, b={affine_b}")
    print(f"密文: {enc_affine}")
    print(f"解密: {dec_affine}")
    print("\n")
    print("2. Playfair密码演示")
    playfair_key = "PLAYFAIR"
    test_text2 = "HELLOWORLD"
    enc_playfair = playfair_cipher(test_text2, playfair_key, mode="encrypt")
    dec_playfair = playfair_cipher(enc_playfair, playfair_key, mode="decrypt")
    print(f"明文: {test_text2}")
    print(f"密钥: {playfair_key}")
    print(f"密文: {enc_playfair}")
    print(f"解密: {dec_playfair}")
    print("\n")
    print("3. 密文穷举破译")
    target_ciphertext = "BEEAKFYDJXUQYHYJQRYHTYJQFBQDUYJIIKFUHCQD"
    brute_force_shift_cipher(target_ciphertext)
    print("\n")