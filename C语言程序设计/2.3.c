#include <stdio.h>

int main() {
    char ch;
    
    printf("请输入拼音首字母查姓氏 (如 a): ");
    scanf(" %c", &ch); // 前面的空格可以忽略之前遗留的换行符
    
    switch (ch) {
        case 'a': case 'A':
            printf("安、艾、阿、敖\n");
            break;
        case 'b': case 'B':
            printf("白、毕、包、班\n");
            break;
        case 'c': case 'C':
            printf("曹、陈、蔡、崔\n");
            break;
        case 'd': case 'D':
            printf("丁、董、杜、戴\n");
            break;
        case 'e': case 'E':
            printf("鄂\n");
            break;
        default:
            printf("其它\n");
            break;
    }
    
    return 0;
}