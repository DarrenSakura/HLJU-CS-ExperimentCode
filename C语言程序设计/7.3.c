#include <stdio.h>

// 自定义字符串连接函数
char* my_strcat(char *dest, char *src) {
    char *p = dest; // 保存目标字符串的首地址，用于最后返回

    // 1. 将指针移动到目标字符串的末尾 (\0 处)
    while (*dest != '\0') {
        dest++;
    }

    // 2. 将源字符串的字符逐个拷贝到目标字符串的末尾
    while (*src != '\0') {
        *dest = *src;
        dest++;
        src++;
    }

    // 3. 补充字符串结束符
    *dest = '\0';

    return p;
}

int main() {
    char str1[200]; // 保证有足够的空间容纳连接后的字符串
    char str2[100];

    printf("请输入目标字符串 (dest): ");
    scanf("%s", str1);
    printf("请输入源字符串 (src): ");
    scanf("%s", str2);

    my_strcat(str1, str2);

    printf("连接后的字符串为: %s\n", str1);

    return 0;
}