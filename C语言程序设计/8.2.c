#include <stdio.h>

// 矩阵转置函数
void transpose(int matrix[3][3]) {
    int temp;
    for (int i = 0; i < 3; i++) {
        // j 从 i + 1 开始，只遍历主对角线右上方的一半元素，与左下方元素交换
        for (int j = i + 1; j < 3; j++) {
            temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
}

// 辅助输出函数
void print_matrix(int matrix[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%4d", matrix[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int mat[3][3];

    printf("请输入 3x3 矩阵的 9 个元素:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            scanf("%d", &mat[i][j]);
        }
    }

    printf("\n原始矩阵:\n");
    print_matrix(mat);

    // 调用转置函数
    transpose(mat);

    printf("\n转置后的矩阵:\n");
    print_matrix(mat);

    return 0;
}