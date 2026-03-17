#include <stdio.h>
#include <string.h>

// 排序函数，参数为指向指针的指针
void sort_strings(char **p, int n) {
    int i, j;
    char *temp;
    for (i = 0; i < n - 1; i++) {
        for (j = i + 1; j < n; j++) {
            // 如果前一个字符串大于后一个字符串，则交换它们的指针
            if (strcmp(*(p + i), *(p + j)) > 0) {
                temp = *(p + i);
                *(p + i) = *(p + j);
                *(p + j) = temp;
            }
        }
    }
}

int main() {
    char str[10][100]; // 存储 10 个字符串，每个最长 99 字符
    char *p[10];       // 指针数组，存储每个字符串的首地址
    int i;

    printf("请输入 10 个字符串:\n");
    for (i = 0; i < 10; i++) {
        scanf("%s", str[i]);
        p[i] = str[i]; // 将指针指向对应的字符串
    }

    // 传入指针数组的首地址（即指向指针的指针）
    sort_strings(p, 10);

    printf("\n排序后的字符串为:\n");
    for (i = 0; i < 10; i++) {
        printf("%s\n", p[i]); // 输出指针指向的字符串
    }

    return 0;
}