#include <stdio.h>

int main() {
    int n;
    printf("请输入杨辉三角形的行数 n: ");
    scanf("%d", &n);

    int arr[n][n];

    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= i; j++) {
            if (j == 0 || j == i) {
                arr[i][j] = 1; // 边缘全为1
            } else {
                arr[i][j] = arr[i - 1][j - 1] + arr[i - 1][j]; // 等于上一行两肩数字之和
            }
            printf("%-4d", arr[i][j]);
        }
        printf("\n");
    }

    return 0;
}