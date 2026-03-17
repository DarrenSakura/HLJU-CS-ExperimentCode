#include <stdio.h>

// (1) 输入 10 个数
void input_array(int *arr, int n) {
    printf("请输入 %d 个整数:\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", arr + i); // 等价于 &arr[i]
    }
}

// (2) 实现具体互换处理，并通过指针返回最大值和最小值
void process_array(int *arr, int n, int *min_val, int *max_val) {
    int min_idx = 0;
    int max_idx = 0;
    int temp;

    // 1. 寻找最小值的下标
    for (int i = 1; i < n; i++) {
        if (*(arr + i) < *(arr + min_idx)) {
            min_idx = i;
        }
    }
    
    // 将最小值与第一个数互换
    temp = *(arr + 0);
    *(arr + 0) = *(arr + min_idx);
    *(arr + min_idx) = temp;

    // 2. 寻找最大值的下标（必须在第一次互换后寻找，以防最大值原本在第一个位置被换走了）
    for (int i = 1; i < n; i++) {
        if (*(arr + i) > *(arr + max_idx)) {
            max_idx = i;
        }
    }
    
    // 将最大值与最后一个数互换
    temp = *(arr + n - 1);
    *(arr + n - 1) = *(arr + max_idx);
    *(arr + max_idx) = temp;

    // 通过指针参数返回最小值和最大值
    *min_val = *(arr + 0);      // 此时第一个数就是最小值
    *max_val = *(arr + n - 1);  // 此时最后一个数就是最大值
}

// (3) 输出 10 个数
void output_array(int *arr, int n) {
    printf("处理后的数组:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", *(arr + i));
    }
    printf("\n");
}

int main() {
    int arr[10];
    int min_value, max_value;
    
    input_array(arr, 10);
    
    // 传入数组及 min_value, max_value 的地址用于接收结果
    process_array(arr, 10, &min_value, &max_value);
    
    printf("由指针返回的结果 -> 最小值: %d, 最大值: %d\n", min_value, max_value);
    output_array(arr, 10);
    
    return 0;
}