def print_multiplication_table(mode='triangle', n=9):
    """
    生成并打印乘法表
    :param mode: 'triangle' (基础三角形) 或 'full' (完整矩形)
    :param n: 乘法表的范围，默认为 9
    """
    if mode == 'triangle':
        # 1. 实现基础三角形格式乘法表
        print(f"\n--- {n}x{n} 基础三角形乘法表 ---")
        for i in range(1, n + 1):          # 外层循环控制行
            for j in range(1, i + 1):      # 内层循环控制列，列数随着行数增加
                # 4. 优化输出格式和对齐：使用 f-string，<3 表示左对齐且占3个字符宽度
                print(f"{j}x{i}={i*j:<3}", end="  ")
            print()  # 换行
            
    elif mode == 'full':
        # 2. 添加完整格式乘法表 (矩形)
        print(f"\n--- {n}x{n} 完整格式乘法表 ---")
        for i in range(1, n + 1):
            for j in range(1, n + 1):      # 内层循环固定为 n 次
                print(f"{j}x{i}={i*j:<3}", end="  ")
            print()

def main():
    while True:
        print("\n=== 乘法表生成器 ===")
        print("1. 生成基础三角形格式乘法表")
        print("2. 生成完整格式乘法表")
        print("3. 退出")
        
        choice = input("请选择操作（1/2/3）：")
        
        if choice == '3':
            print("退出程序，再见！")
            break
            
        if choice in ['1', '2']:
            try:
                # 3. 实现可定制范围功能
                n_input = input("请输入乘法表的范围 (默认按回车为 9): ")
                n = int(n_input) if n_input.strip() else 9
                
                if n <= 0:
                    print("错误：请输入一个正整数！")
                    continue
                    
                if choice == '1':
                    print_multiplication_table(mode='triangle', n=n)
                elif choice == '2':
                    print_multiplication_table(mode='full', n=n)
                    
            except ValueError:
                print("错误：输入无效，请输入一个整数数字！")
        else:
            print("无效的选择，请重新输入！")

if __name__ == "__main__":
    main()