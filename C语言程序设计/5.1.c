#include <stdio.h>

void input(int arr[], int n) {
    printf("请输入 %d 个整数:\n", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
}

void selection_sort(int arr[], int n) {
    int i, j, min_idx, temp;
    for (i = 0; i < n - 1; i++) {
        min_idx = i;
        for (j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            temp = arr[i]; arr[i] = arr[min_idx]; arr[min_idx] = temp;
        }
    }
}

void output(int arr[], int n) {
    printf("排序后的数组:\n");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int arr[10];
    input(arr, 10);
    selection_sort(arr, 10);
    output(arr, 10);
    return 0;
}