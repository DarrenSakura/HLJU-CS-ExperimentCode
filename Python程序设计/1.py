def calculator():
    print("--- 欢迎使用简易计算器 ---")
    print("支持的运算符：+, -, *, /")
    
    try:
        # 1. 使用 input() 获取用户输入，并尝试转换为浮点数
        num1 = float(input("请输入第一个数字："))
        operator = input("请输入运算符（+、-、*、/）：")
        num2 = float(input("请输入第二个数字："))
        
        # 2. 使用条件判断处理不同运算符
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            # 3. 添加异常处理机制：防止除数为0
            if num2 == 0:
                raise ZeroDivisionError("除数不能为零（0）！")
            result = num1 / num2
        else:
            print("错误：输入的运算符不正确！")
            return
            
        # 4. 输出计算结果
        print(f"计算结果：{num1} {operator} {num2} = {result}")
        
    except ValueError:
        # 捕获用户输入非数字字符时的异常
        print("输入错误：请输入有效的数字！")
    except ZeroDivisionError as e:
        # 捕获除数为零的异常
        print(f"计算错误：{e}")
    except Exception as e:
        # 捕获其他未知异常
        print(f"发生未知错误：{e}")

# 5. 测试各种输入情况（调用函数）
if __name__ == "__main__":
    while True:
        calculator()
        
        # 询问用户是否继续测试
        cont = input("\n是否继续计算？(输入 'q' 退出，其他键继续): ")
        if cont.lower() == 'q':
            print("退出计算器，再见！")
            break
        print("-" * 30)