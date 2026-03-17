#include <stdio.h>

// (1) 输入 n 个数
void input(int *arr, int n) {
    printf("请输入 %d 个整数:\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", arr + i);
    }
}

// (2) 实现逆序排列 (纯指针操作)
void reverse(int *arr, int n) {
    int *left = arr;            // 指向数组第一个元素
    int *right = arr + n - 1;   // 指向数组最后一个元素
    int temp;

    while (left < right) {
        // 交换左右指针指向的值
        temp = *left;
        *left = *right;
        *right = temp;
        
        // 指针向中间移动
        left++;
        right--;
    }
}

// (3) 输出逆序排列后的 n 个数
void output(int *arr, int n) {
    printf("逆序排列后的数组:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", *(arr + i));
    }
    printf("\n");
}

int main() {
    int n;
    printf("请输入元素个数 n: ");
    scanf("%d", &n);
    
    // 假设最多允许100个元素，也可以用动态内存分配(malloc)
    int arr[100]; 
    
    input(arr, n);
    reverse(arr, n);
    output(arr, n);
    
    return 0;
}