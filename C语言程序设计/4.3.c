#include <stdio.h>

// 递归求 x^n
float power_recursive(float x, int n) {
    if (n == 0) return 1;
    if (n > 0) return x * power_recursive(x, n - 1);
    return 1.0 / power_recursive(x, -n); // 支持负指数
}

// 非递归求 x^n
float power_iterative(float x, int n) {
    float result = 1.0;
    int abs_n = n > 0 ? n : -n;
    
    for (int i = 0; i < abs_n; i++) {
        result *= x;
    }
    return n >= 0 ? result : 1.0 / result;
}

int main() {
    float x;
    int n;
    printf("请输入底数 x 和指数 n (用空格分隔): ");
    scanf("%f %d", &x, &n);
    
    printf("递归计算结果: %f^%d = %.6f\n", x, n, power_recursive(x, n));
    printf("非递归计算结果: %f^%d = %.6f\n", x, n, power_iterative(x, n));
    
    return 0;
}