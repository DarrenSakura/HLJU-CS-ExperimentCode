#include <stdio.h>

// 递归求阶乘
long long fact_recursive(int n) {
    if (n <= 1) return 1;
    return n * fact_recursive(n - 1);
}

// 非递归求阶乘
long long fact_iterative(int n) {
    long long result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    printf("10 以内的阶乘:\n");
    for (int i = 1; i <= 10; i++) {
        printf("%2d! = %-8lld (递归) | %-8lld (非递归)\n", 
               i, fact_recursive(i), fact_iterative(i));
    }
    return 0;
}