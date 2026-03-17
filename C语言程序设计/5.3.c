#include <stdio.h>

int main() {
    int arr[11] = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19}; // 预留一个位置
    int num, i, j;

    printf("原数组: ");
    for (i = 0; i < 10; i++) printf("%d ", arr[i]);
    
    printf("\n请输入要插入的数: ");
    scanf("%d", &num);

    // 从后往前查找插入位置并移动元素
    for (i = 9; i >= 0; i--) {
        if (arr[i] > num) {
            arr[i + 1] = arr[i]; // 向后移位
        } else {
            break;
        }
    }
    arr[i + 1] = num; // 插入

    printf("插入后的数组: ");
    for (i = 0; i < 11; i++) printf("%d ", arr[i]);
    printf("\n");

    return 0;
}