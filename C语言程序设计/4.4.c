#include <stdio.h>

// 递归函数求质数因子
// n: 待分解的数, divisor: 当前除数（从2开始尝试）
void find_factors(int n, int divisor) {
    if (n <= 1) return; // 递归终点
    
    if (n % divisor == 0) {
        printf("%d", divisor);
        if (n / divisor > 1) {
            printf("*"); // 如果除完之后大于1，说明还有后续因子
        }
        find_factors(n / divisor, divisor); // 继续用当前除数去试除
    } else {
        find_factors(n, divisor + 1); // 不能整除，尝试下一个因子
    }
}

int main() {
    int n;
    printf("请输入一个自然数 (n > 1): ");
    scanf("%d", &n);
    
    if (n > 1) {
        printf("%d = ", n);
        find_factors(n, 2); // 从最小的质数 2 开始除
        printf("\n");
    } else {
        printf("请输入大于1的自然数。\n");
    }
    
    return 0;
}