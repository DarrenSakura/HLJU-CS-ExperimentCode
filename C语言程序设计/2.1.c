#include <stdio.h>

int main() {
    float a, b, c, temp;
    
    printf("请输入3个数（用空格分隔）: ");
    scanf("%f %f %f", &a, &b, &c);
    
    // 比较并交换，确保 a <= b
    if (a > b) {
        temp = a; a = b; b = temp;
    }
    // 比较并交换，确保 a <= c
    if (a > c) {
        temp = a; a = c; c = temp;
    }
    // 比较并交换，确保 b <= c
    if (b > c) {
        temp = b; b = c; c = temp;
    }
    
    printf("从小到大输出: %.2f %.2f %.2f\n", a, b, c);
    
    return 0;
}