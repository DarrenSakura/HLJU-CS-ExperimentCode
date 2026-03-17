#include <stdio.h>

int main() {
    int i, j, space;

    printf("1. 左下三角（标准形式）:\n");
    for (i = 1; i <= 9; i++) {
        for (j = 1; j <= i; j++) {
            printf("%d*%d=%-2d ", j, i, i * j); // %-2d 表示左对齐，占两个字符宽度
        }
        printf("\n");
    }

    printf("\n2. 左上三角:\n");
    for (i = 9; i >= 1; i--) {
        for (j = 1; j <= i; j++) {
            printf("%d*%d=%-2d ", j, i, i * j);
        }
        printf("\n");
    }

    printf("\n3. 右下三角:\n");
    for (i = 1; i <= 9; i++) {
        // 打印前面的空格占位（每项 7 个空格）
        for (space = 1; space <= 9 - i; space++) {
            printf("       "); 
        }
        // 打印乘法式
        for (j = 1; j <= i; j++) {
            printf("%d*%d=%-2d ", j, i, i * j);
        }
        printf("\n");
    }

    printf("\n4. 右上三角:\n");
    for (i = 9; i >= 1; i--) {
        // 打印前面的空格占位
        for (space = 1; space <= 9 - i; space++) {
            printf("       ");
        }
        // 打印乘法式
        for (j = 1; j <= i; j++) {
            printf("%d*%d=%-2d ", j, i, i * j);
        }
        printf("\n");
    }

    return 0;
}