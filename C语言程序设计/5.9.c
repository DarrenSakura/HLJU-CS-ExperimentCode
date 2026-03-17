#include <stdio.h>

void reverse(int arr[], int start, int end) {
    while (start < end) {
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
}

// 实现右移：整体反转 -> 反转前K个 -> 反转剩余的
void right_shift(int arr[], int n, int k) {
    k = k % n; // 防止 k > n
    if (k == 0) return;
    reverse(arr, 0, n - 1);
    reverse(arr, 0, k - 1);
    reverse(arr, k, n - 1);
}

int main() {
    int n, k;
    printf("请输入数组长度 n: ");
    scanf("%d", &n);
    
    int arr[100];
    printf("请输入 %d 个元素:\n", n);
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);

    printf("请输入右移位数 k: ");
    scanf("%d", &k);

    right_shift(arr, n, k);

    printf("右移后的数组:\n");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");

    return 0;
}