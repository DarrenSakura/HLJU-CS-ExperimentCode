#include <stdio.h>

int main() {
    int a, b, c; // 分别表示百位、十位、个位

    printf("100-999之间的水仙花数有:\n");
    
    for (int i = 100; i <= 999; i++) {
        a = i / 100;         // 提取百位
        b = (i / 10) % 10;   // 提取十位
        c = i % 10;          // 提取个位
        
        // 判断各位数字的立方和是否等于本身
        if (a * a * a + b * b * b + c * c * c == i) {
            printf("%d\n", i);
        }
    }

    return 0;
}