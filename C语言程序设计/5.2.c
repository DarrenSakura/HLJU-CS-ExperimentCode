#include <stdio.h>

void input_matrix(int mat[3][3]) {
    printf("请输入 3x3 矩阵的 9 个元素:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            scanf("%d", &mat[i][j]);
        }
    }
}

void find_max(int mat[3][3], int *max_val, int *row, int *col) {
    *max_val = mat[0][0];
    *row = 0;
    *col = 0;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (mat[i][j] > *max_val) {
                *max_val = mat[i][j];
                *row = i;
                *col = j;
            }
        }
    }
}

void output_result(int max_val, int row, int col) {
    printf("最大元素为 %d, 位于第 %d 行, 第 %d 列\n", max_val, row + 1, col + 1);
}

int main() {
    int mat[3][3];
    int max_val, row, col;
    input_matrix(mat);
    find_max(mat, &max_val, &row, &col);
    output_result(max_val, row, col);
    return 0;
}