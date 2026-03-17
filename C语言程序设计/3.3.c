#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int num1, num2, op_choice;
    int user_answer, correct_answer;
    int score;
    double accuracy;
    char operators[] = {'+', '-', '*', '/'};
    
    srand((unsigned int)time(NULL)); // 初始化随机数种子

    while (1) {
        score = 0;
        printf("=== 开始10道四则运算测试 ===\n");
        
        for (int i = 1; i <= 10; i++) {
            num1 = rand() % 10 + 1; // 1~10 的随机正整数
            num2 = rand() % 10 + 1;
            op_choice = rand() % 4; // 0:加, 1:减, 2:乘, 3:除

            // 为了保证整除运算对小学生友好，如果是除法，将 num1 变为 num1*num2
            if (op_choice == 3) {
                num1 = num1 * num2; 
            }

            printf("第 %d 题: %d %c %d = ?\n", i, num1, operators[op_choice], num2);
            printf("请输入答案: ");
            scanf("%d", &user_answer);

            switch (op_choice) {
                case 0: correct_answer = num1 + num2; break;
                case 1: correct_answer = num1 - num2; break;
                case 2: correct_answer = num1 * num2; break;
                case 3: correct_answer = num1 / num2; break;
            }

            if (user_answer == correct_answer) {
                printf("Right!\n\n");
                score += 10; // 每题10分
            } else {
                printf("Wrong!\n\n");
            }
        }

        accuracy = (score / 100.0) * 100; // 计算正确率
        printf("测试结束！您的总分是: %d 分\n", score);
        printf("您的回答正确率: %.2f%%\n", accuracy);

        if (accuracy >= 75.0) {
            printf("恭喜您，正确率达标，退出练习！\n");
            break; // 正确率 >= 75%，退出循环
        } else {
            printf("正确率低于 75%%，请继续努力，重新开始练习...\n\n");
        }
    }

    return 0;
}