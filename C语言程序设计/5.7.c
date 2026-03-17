#include <stdio.h>

void input(int arr[], int n) {
    printf("请输入 %d 个整数:\n", n);
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);
}

void bubble_sort(int arr[], int n) {
    int temp;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j]; arr[j] = arr[j + 1]; arr[j + 1] = temp;
            }
        }
    }
}

void output(int arr[], int n) {
    printf("排序后的数组:\n");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int n;
    printf("请输入元素个数 n: ");
    scanf("%d", &n);
    int arr[100]; // 假设最多100个
    input(arr, n);
    bubble_sort(arr, n);
    output(arr, n);
    return 0;
}