#include <stdio.h>

int main() {
    // 定义5种颜色的字符串数组
    char *colors[] = {"红", "黄", "蓝", "白", "黑"};
    int count = 0; // 记录总的可能取法数

    printf("从红、黄、蓝、白、黑中先后取出3个不同颜色球的排列情况:\n");
    printf("--------------------------------------------------\n");

    // i 表示第���次取出的球，j 表示第二次，k 表示第三次
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            for (int k = 0; k < 5; k++) {
                // 判断三次取出的球颜色是否都互不相同
                if (i != j && i != k && j != k) {
                    count++;
                    printf("第 %2d 种: %s, %s, %s\n", count, colors[i], colors[j], colors[k]);
                }
            }
        }
    }

    printf("--------------------------------------------------\n");
    printf("总共有 %d 种不同的取法。\n", count);

    return 0;
}