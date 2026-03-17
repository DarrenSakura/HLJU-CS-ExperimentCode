# 1. 导入random模块
import random

def guess_number_game():
    print("--- 欢迎来到猜数字游戏 ---")
    print("我已经想好了一个 1 到 100 之间的整数。")
    
    # 2. 生成随机目标数字
    target_number = random.randint(1, 100)
    
    # 3. 设置游戏循环和尝试次数
    max_attempts = 7  # 限制最多猜7次
    attempts = 0
    
    print(f"你有 {max_attempts} 次机会来猜出这个数字。\n")

    # 游戏主循环
    while attempts < max_attempts:
        attempts += 1
        
        # 4. 实现用户输入和验证
        try:
            user_input = input(f"第 {attempts} 次猜想，请输入你的数字：")
            guess = int(user_input)
            
            # 验证输入范围
            if guess < 1 or guess > 100:
                print("提示：请输入 1 到 100 之间的有效数字！")
                attempts -= 1 # 输入无效不计入尝试次数
                continue
                
        except ValueError:
            print("错误：请输入一个有效的整数！")
            attempts -= 1 # 输入无效不计入尝试次数
            continue
            
        # 5. 添加游戏提示和反馈
        if guess < target_number:
            print("提示：你猜的数字太小了！⬇️\n")
        elif guess > target_number:
            print("提示：你猜的数字太大了！⬆️\n")
        else:
            print(f"🎉 恭喜你！猜对了！目标数字就是 {target_number}。")
            print(f"你总共用了 {attempts} 次机会。")
            break  # 猜对后跳出循环
            
    # 如果循环结束（次数用完）且没猜对
    if guess != target_number:
        print(f"很遗憾，{max_attempts} 次机会已用完。")
        print(f"正确的数字是：{target_number}。游戏结束！")

if __name__ == "__main__":
    while True:
        guess_number_game()
        
        # 询问用户是否再玩一局
        cont = input("\n想再玩一局吗？(输入 'y' 继续，其他键退出): ")
        if cont.lower() != 'y':
            print("感谢游玩，再见！")
            break
        print("=" * 40)