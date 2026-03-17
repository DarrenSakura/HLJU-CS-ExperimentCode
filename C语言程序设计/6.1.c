#include <stdio.h>

// 通过指针互换两个变量的值
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x, y;
    
    printf("请输入两个整数 (用空格分隔): ");
    scanf("%d %d", &x, &y);
    
    printf("交换前: x = %d, y = %d\n", x, y);
    
    // 传入 x 和 y 的地址
    swap(&x, &y);
    
    printf("交换后: x = %d, y = %d\n", x, y);
    
    return 0;
}