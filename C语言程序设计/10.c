#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 定义学生信息的链表节点结构体
struct Student {
    int id;               // 学号
    char name[20];        // 姓名
    char gender[10];      // 性别
    int age;              // 年龄
    float c_score;        // C语言成绩
    struct Student *next; // 指向下一个节点的指针
};

// (1) 插入节点，要求链表始终按【学号从小到大】的顺序排列
struct Student* insert_sorted(struct Student *head) {
    // 动态分配新节点内存
    struct Student *new_node = (struct Student*)malloc(sizeof(struct Student));
    if (new_node == NULL) {
        printf("内存分配失败！\n");
        return head;
    }

    printf("\n--- 录入学生信息 ---\n");
    printf("请输入学号: "); scanf("%d", &new_node->id);
    printf("请输入姓名: "); scanf("%s", new_node->name);
    printf("请输入性别: "); scanf("%s", new_node->gender);
    printf("请输入年龄: "); scanf("%d", &new_node->age);
    printf("请输入C语言成绩: "); scanf("%f", &new_node->c_score);
    new_node->next = NULL;

    // 情况 A：链表为空，或者新节点的学号小于当前头节点的学号，插在头部
    if (head == NULL || head->id > new_node->id) {
        new_node->next = head;
        printf("插入成功！\n");
        return new_node; // 新节点成为新的头节点
    }

    // 情况 B：遍历链表寻找合适的插入位置（保证学号升序）
    struct Student *current = head;
    while (current->next != NULL && current->next->id < new_node->id) {
        current = current->next;
    }

    // 防止输入重复的学号
    if (current->id == new_node->id || (current->next != NULL && current->next->id == new_node->id)) {
        printf("学号 %d 已存在，插入失败！\n", new_node->id);
        free(new_node); // 释放刚才分配的内存
        return head;
    }

    // 找到位置，在 current 之后插入 new_node
    new_node->next = current->next;
    current->next = new_node;
    printf("插入成功！\n");
    
    return head;
}

// (2) 删除指定学号的学生信息
struct Student* delete_node(struct Student *head, int target_id) {
    if (head == NULL) {
        printf("链表为空，无法删除！\n");
        return head;
    }

    // 情况 A：要删除的是头节点
    if (head->id == target_id) {
        struct Student *temp = head;
        head = head->next; // 头指针后移
        free(temp);        // 释放原头节点内存
        printf("学号为 %d 的学生信息已成功删除！\n", target_id);
        return head;
    }

    // 情况 B：要删除的节点在链表中间或尾部
    struct Student *current = head;
    while (current->next != NULL && current->next->id != target_id) {
        current = current->next;
    }

    // 判断是否找到目标节点
    if (current->next == NULL) {
        printf("未找到学号为 %d 的学生！\n", target_id);
    } else {
        struct Student *temp = current->next;
        current->next = temp->next; // 绕过要删除的节点
        free(temp);                 // 释放内存
        printf("学号为 %d 的学生信息已成功删除！\n", target_id);
    }

    return head;
}

// 辅助功能：打印输出链表所有节点
void print_list(struct Student *head) {
    if (head == NULL) {
        printf("\n当前链表为空！\n");
        return;
    }
    
    printf("\n--- 学生信息列表 ---\n");
    printf("%-10s %-10s %-6s %-6s %-10s\n", "��号", "姓名", "性别", "年龄", "C语言成绩");
    struct Student *current = head;
    while (current != NULL) {
        printf("%-10d %-10s %-6s %-6d %-10.2f\n", 
               current->id, current->name, current->gender, current->age, current->c_score);
        current = current->next;
    }
}

// 主函数：菜单驱动测试
int main() {
    struct Student *head = NULL; // 初始化空链表
    int choice;
    int target_id;

    while (1) {
        printf("\n========= 学生信息链表管理系统 =========\n");
        printf("1. 插入学生信息 (自动按学号升序排序)\n");
        printf("2. 删除学生信息 (按学号删除)\n");
        printf("3. 打印全体学生信息\n");
        printf("0. 退出系统\n");
        printf("=======================================\n");
        printf("请输入您的选择 (0-3): ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                head = insert_sorted(head);
                break;
            case 2:
                printf("请输入要删除的学生学号: ");
                scanf("%d", &target_id);
                head = delete_node(head, target_id);
                break;
            case 3:
                print_list(head);
                break;
            case 0:
                printf("退出系统！\n");
                // 退出前应释放所有链表节点内存，这里作为基础示例省略了销毁整个链表的过程
                return 0;
            default:
                printf("输入无效，请重新选择。\n");
        }
    }
    return 0;
}