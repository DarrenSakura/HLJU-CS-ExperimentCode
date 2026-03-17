#include <stdio.h>

int main() {
    int mat[3][3];
    int sum_main = 0, sum_anti = 0;

    printf("请输入 3x3 矩阵的 9 个元素:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            scanf("%d", &mat[i][j]);
            if (i == j) sum_main += mat[i][j];             // 主对角线
            if (i + j == 2) sum_anti += mat[i][j];         // 副对角线
        }
    }

    printf("主对角线元素之和: %d\n", sum_main);
    printf("副对角线元素之和: %d\n", sum_anti);
    return 0;
}