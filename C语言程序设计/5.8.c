#include <stdio.h>

void input_arr(int arr[], int n) {
    printf("请按从小到大的顺序输入 %d 个整数:\n", n);
    for (int i = 0; i < n; i++) scanf("%d", &arr[i]);
}

// 非递归二分查找
int binary_search_iterative(int arr[], int left, int right, int x) {
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == x) return mid;
        if (arr[mid] < x) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

// 递归二分查找
int binary_search_recursive(int arr[], int left, int right, int x) {
    if (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == x) return mid;
        if (arr[mid] < x) return binary_search_recursive(arr, mid + 1, right, x);
        return binary_search_recursive(arr, left, mid - 1, x);
    }
    return -1;
}

void output_result(int index) {
    if (index != -1) printf("查找到元素，索引位置为: %d\n", index);
    else printf("未找到该元素。\n");
}

int main() {
    int n, x;
    printf("请输入数组长度 n: ");
    scanf("%d", &n);
    int arr[100];
    
    input_arr(arr, n);
    
    printf("请输入要查找的值 x: ");
    scanf("%d", &x);

    printf("\n--- 非递归查找结果 ---\n");
    output_result(binary_search_iterative(arr, 0, n - 1, x));

    printf("\n--- 递归查找结果 ---\n");
    output_result(binary_search_recursive(arr, 0, n - 1, x));

    return 0;
}