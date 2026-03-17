#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// 基础功能函数声明
int generate_random();
int check_answer(int correct, int user);
void statistics(int correct_count, int total_count, int *score, float *accuracy);
void generate_division(int *num1, int *num2); // 判断除法合法性的选作功能

// 任务函数声明
void task1();
void task2();
void task3();
void task4();
void task5();

int main() {
    int choice;
    srand((unsigned int)time(NULL));

    while (1) {
        printf("\n******************************************************************************\n");
        printf("* 1. 任务1：随机产生1-10 之间正整数，出乘法问题，直到学生答对为止。        *\n");
        printf("* 2. 任务2：在任务1 基础上，当学生答错时，最多给三次机会。                   *\n");
        printf("* 3. 任务3：在任务1 基础上，连做10 道乘法题，不给机会重做，统计总分、正确率。*\n");
        printf("* 4. 任务4：在任务3 基础上，随机产生10 道四则运算题，不给机会重做，          *\n");
        printf("*    统计总分、正确率。                                                      *\n");
        printf("* 5. 任务5：在任务4 基础上，若回答正确率低于 75%%，则再做10 道题，            *\n");
        printf("*    直到正确率高于 75%%为止。                                                *\n");
        printf("* 6. 退出                                                                    *\n");
        printf("******************************************************************************\n");
        printf("请选择任务 (1-6): ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: task1(); break;
            case 2: task2(); break;
            case 3: task3(); break;
            case 4: task4(); break;
            case 5: task5(); break;
            case 6: printf("退出系统。\n"); return 0;
            default: printf("输入无效，请重新输入！\n");
        }
    }
    return 0;
}

// 产生 1-10 之间的随机数
int generate_random() {
    return rand() % 10 + 1;
}

// 判断答题是否正确
int check_answer(int correct, int user) {
    return correct == user ? 1 : 0;
}

// 成绩统计函数
void statistics(int correct_count, int total_count, int *score, float *accuracy) {
    *score = correct_count * 10;
    *accuracy = ((float)correct_count / total_count) * 100;
}

// 保证除法能整除的函数
void generate_division(int *num1, int *num2) {
    *num2 = generate_random();
    int temp = generate_random();
    *num1 = (*num2) * temp; // 保证 num1 是 num2 的倍数
}

// 任务 1
void task1() {
    int num1 = generate_random();
    int num2 = generate_random();
    int ans;
    printf("题目: %d * %d = ?\n", num1, num2);
    while (1) {
        printf("请输入答案: ");
        scanf("%d", &ans);
        if (check_answer(num1 * num2, ans)) {
            printf("Right!\n");
            break;
        } else {
            printf("Wrong! Please try again.\n");
        }
    }
}

// 任务 2
void task2() {
    int num1 = generate_random();
    int num2 = generate_random();
    int ans, tries = 0;
    printf("题目: %d * %d = ?\n", num1, num2);
    while (tries < 3) {
        printf("请输入答案: ");
        scanf("%d", &ans);
        if (check_answer(num1 * num2, ans)) {
            printf("Right!\n");
            return;
        } else {
            tries++;
            if (tries < 3) {
                printf("Wrong! Please try again.\n");
            }
        }
    }
    printf("Wrong! You have tried three times! Test over!\n");
}

// 任务 3
void task3() {
    int num1, num2, ans, correct_count = 0;
    int score;
    float accuracy;
    for (int i = 1; i <= 10; i++) {
        num1 = generate_random();
        num2 = generate_random();
        printf("第 %d 题: %d * %d = ?\n请输入答案: ", i, num1, num2);
        scanf("%d", &ans);
        if (check_answer(num1 * num2, ans)) {
            printf("Right!\n");
            correct_count++;
        } else {
            printf("Wrong!\n");
        }
    }
    statistics(correct_count, 10, &score, &accuracy);
    printf("总分: %d, 正确率: %.2f%%\n", score, accuracy);
}

// 任务 4
void task4() {
    int num1, num2, ans, correct_count = 0, op, correct_ans;
    int score;
    float accuracy;
    char ops[] = {'+', '-', '*', '/'};

    for (int i = 1; i <= 10; i++) {
        op = rand() % 4;
        if (op == 3) {
            generate_division(&num1, &num2); // 调用除法处理
            correct_ans = num1 / num2;
        } else {
            num1 = generate_random();
            num2 = generate_random();
            if (op == 0) correct_ans = num1 + num2;
            else if (op == 1) correct_ans = num1 - num2;
            else correct_ans = num1 * num2;
        }

        printf("第 %d 题: %d %c %d = ?\n请输入答案: ", i, num1, ops[op], num2);
        scanf("%d", &ans);
        if (check_answer(correct_ans, ans)) {
            printf("Right!\n");
            correct_count++;
        } else {
            printf("Wrong!\n");
        }
    }
    statistics(correct_count, 10, &score, &accuracy);
    printf("总分: %d, 正确率: %.2f%%\n", score, accuracy);
}

// 任务 5
void task5() {
    int num1, num2, ans, correct_count, op, correct_ans;
    int score;
    float accuracy = 0.0;
    char ops[] = {'+', '-', '*', '/'};

    do {
        correct_count = 0;
        printf("\n--- 开始新的一轮10道题测试 ---\n");
        for (int i = 1; i <= 10; i++) {
            op = rand() % 4;
            if (op == 3) {
                generate_division(&num1, &num2);
                correct_ans = num1 / num2;
            } else {
                num1 = generate_random();
                num2 = generate_random();
                if (op == 0) correct_ans = num1 + num2;
                else if (op == 1) correct_ans = num1 - num2;
                else correct_ans = num1 * num2;
            }

            printf("第 %d 题: %d %c %d = ?\n请输入答案: ", i, num1, ops[op], num2);
            scanf("%d", &ans);
            if (check_answer(correct_ans, ans)) {
                printf("Right!\n");
                correct_count++;
            } else {
                printf("Wrong!\n");
            }
        }
        statistics(correct_count, 10, &score, &accuracy);
        printf("本轮总分: %d, 正确率: %.2f%%\n", score, accuracy);
        
        if (accuracy < 75.0) {
            printf("正确率低于 75%%，请重新进行测试！\n");
        }
    } while (accuracy < 75.0);
    
    printf("正确率达标，任务完成！\n");
}