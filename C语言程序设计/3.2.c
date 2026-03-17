#include <stdio.h>
#include <math.h>

int main() {
    int count = 0; // 记录素数个数，用于控制换行

    for (int i = 2; i <= 100; i++) {
        int is_prime = 1;
        for (int j = 2; j <= sqrt(i); j++) {
            if (i % j == 0) {
                is_prime = 0;
                break;
            }
        }
        
        if (is_prime) {
            printf("%6d", i); // 每个数占6位
            count++;
            if (count % 5 == 0) { // 每5个数换行
                printf("\n");
            }
        }
    }
    
    // 如果最后一行不足5个，补一个换行符
    if (count % 5 != 0) {
        printf("\n");
    }
    
    return 0;
}