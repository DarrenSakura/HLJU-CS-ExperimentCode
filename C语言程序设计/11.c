#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define N 5 // 学生人数

// 定义学生结构体
struct Student {
    int id;               // 学号
    char name[20];        // 姓名
    float scores[3];      // 3门课成绩
    float average;        // 平均成绩
};

// 1. 将以 '$' 结束的字符串写入 char.dat
void write_char_file() {
    FILE *fp;
    char ch;

    if ((fp = fopen("char.dat", "w")) == NULL) {
        printf("无法创建文件 char.dat\n");
        exit(1);
    }

    printf("【任务1】请输入一串字符（以 '$' 结束）:\n");
    // 不断读取字符直到遇到 '$'
    while ((ch = getchar()) != '$') {
        fputc(ch, fp);
    }
    fclose(fp);
    
    // 清空缓冲区中多余的字符（如回车），以免影响后续输入
    while (getchar() != '\n'); 
    printf("-> 字符串已成功保存到 char.dat 中。\n\n");
}

// 2. 从 char.dat 读出，小写转大写并输出屏幕
void read_char_file_to_upper() {
    FILE *fp;
    char ch;

    if ((fp = fopen("char.dat", "r")) == NULL) {
        printf("无法打开文件 char.dat\n");
        exit(1);
    }

    printf("【任务2】从 char.dat 读出并转为大写的结果:\n");
    while ((ch = fgetc(fp)) != EOF) {
        // 如果是小写字母则转大写，或者直接使用 toupper(ch)
        if (ch >= 'a' && ch <= 'z') {
            ch = ch - 32; 
        }
        putchar(ch);
    }
    printf("\n\n");
    fclose(fp);
}

// 3. 录入5个学生信息，计算平均分并写入 STUD.dat
void write_student_file() {
    FILE *fp;
    struct Student stus[N];

    if ((fp = fopen("STUD.dat", "wb")) == NULL) {
        printf("无法创建文件 STUD.dat\n");
        exit(1);
    }

    printf("【任务3】请输入 %d 个学生的信息:\n", N);
    for (int i = 0; i < N; i++) {
        printf("第 %d 个学生 -> 学号: ", i + 1);
        scanf("%d", &stus[i].id);
        printf("姓名: ");
        scanf("%s", stus[i].name);
        printf("3门课成绩(用空格隔开): ");
        scanf("%f %f %f", &stus[i].scores[0], &stus[i].scores[1], &stus[i].scores[2]);
        
        // 计算平均成绩
        stus[i].average = (stus[i].scores[0] + stus[i].scores[1] + stus[i].scores[2]) / 3.0;
    }

    // 将结构体数组一次性以二进制方式写入文件
    fwrite(stus, sizeof(struct Student), N, fp);
    fclose(fp);
    printf("-> %d 个学生的数据已成功保存到 STUD.dat 磁盘文件中。\n\n", N);
}

// 4. 输入学号，从 STUD.dat 中读取并显示该学生信息
void read_student_by_id() {
    FILE *fp;
    struct Student temp;
    int target_id;
    int found = 0;

    if ((fp = fopen("STUD.dat", "rb")) == NULL) {
        printf("无法打开文件 STUD.dat\n");
        exit(1);
    }

    printf("【任务4】请输入要查询的学生学号: ");
    scanf("%d", &target_id);

    // 每次从文件中读取 1 个 Student 结构体大小的数据
    while (fread(&temp, sizeof(struct Student), 1, fp) == 1) {
        if (temp.id == target_id) {
            printf("\n--- 找到该学生信息 ---\n");
            printf("学号: %d\n", temp.id);
            printf("姓名: %s\n", temp.name);
            printf("成绩1: %.2f, 成绩2: %.2f, 成绩3: %.2f\n", temp.scores[0], temp.scores[1], temp.scores[2]);
            printf("平均成绩: %.2f\n", temp.average);
            found = 1;
            break; // 找到后即可退出循环
        }
    }

    if (!found) {
        printf("未在文件 STUD.dat 中找到学号为 %d 的学生。\n", target_id);
    }

    fclose(fp);
}

int main() {
    // 按题目要求依次执行四个操作
    write_char_file();           // 任务 1
    read_char_file_to_upper();   // 任务 2
    write_student_file();        // 任务 3
    read_student_by_id();        // 任务 4

    return 0;
}