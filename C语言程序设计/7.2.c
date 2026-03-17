#include <stdio.h>

// 自定义字符串比较函数
int strcmp1(char *p1, char *p2) {
    // 当两个字符相等，且没有到达字符串结尾时，继续比较下一个字符
    while (*p1 != '\0' && *p2 != '\0' && *p1 == *p2) {
        p1++;
        p2++;
    }
    // 返回不同字符的 ASCII 码差值
    // 若完全相同则此时 *p1 和 *p2 都是 '\0'，差值为 0
    return *p1 - *p2;
}

int main() {
    char str1[100], str2[100];
    int result;

    printf("请输入第一个字符串: ");
    scanf("%s", str1);
    printf("请输入第二个字符串: ");
    scanf("%s", str2);

    result = strcmp1(str1, str2);

    if (result == 0) {
        printf("结果: str1 和 str2 相等 (返回值为 0)\n");
    } else if (result > 0) {
        printf("结果: str1 大于 str2 (返回值为 %d)\n", result);
    } else {
        printf("结果: str1 小于 str2 (返回值为 %d)\n", result);
    }

    return 0;
}