#include <stdio.h>
#include <string.h>

#define N 10 // 学生总人数

// 定义出生日期结构体
struct Date {
    int year;
    int month;
    int day;
};

// 定义学生信息结构体
struct Student {
    char id[20];            // 学号
    char name[20];          // 姓名
    char gender[10];        // 性别
    struct Date birth;      // 出生年月日
    float score_c;          // C语言成绩
    float score_math;       // 高等数学成绩
    float score_algebra;    // 线性代数成绩
    float average;          // 平均成绩
    int rank;               // 名次
};

// (2) 输入学生基本信息及成绩
void input_students(struct Student stu[], int n) {
    printf("请输入 %d 名学生的信息:\n", n);
    for (int i = 0; i < n; i++) {
        printf("\n--- 第 %d 名学生 ---\n", i + 1);
        printf("学号: "); scanf("%s", stu[i].id);
        printf("姓名: "); scanf("%s", stu[i].name);
        printf("性别: "); scanf("%s", stu[i].gender);
        printf("出生日期(年 月 日，用空格隔开): "); 
        scanf("%d %d %d", &stu[i].birth.year, &stu[i].birth.month, &stu[i].birth.day);
        printf("三门成绩(C语言 高数 ��代，用空格隔开): "); 
        scanf("%f %f %f", &stu[i].score_c, &stu[i].score_math, &stu[i].score_algebra);
    }
}

// (3) 求每个学生三门课程的平均分
void calc_average(struct Student stu[], int n) {
    for (int i = 0; i < n; i++) {
        stu[i].average = (stu[i].score_c + stu[i].score_math + stu[i].score_algebra) / 3.0;
    }
}

// (4) 按平均分排队并确定名次 (降序排序)
void sort_students(struct Student stu[], int n) {
    struct Student temp;
    // 使用冒泡排序
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (stu[j].average < stu[j + 1].average) {
                temp = stu[j];
                stu[j] = stu[j + 1];
                stu[j + 1] = temp;
            }
        }
    }
    // 排序后分配名次
    for (int i = 0; i < n; i++) {
        stu[i].rank = i + 1;
    }
}

// 输出学生列表（用于验证排序结果）
void print_students(struct Student stu[], int n) {
    printf("\n--- 按平均分排名的学生列表 ---\n");
    printf("%-5s %-10s %-10s %-5s %-8s\n", "名次", "学号", "姓名", "平均分", "性别");
    for (int i = 0; i < n; i++) {
        printf("%-5d %-10s %-10s %-6.2f %-8s\n", 
               stu[i].rank, stu[i].id, stu[i].name, stu[i].average, stu[i].gender);
    }
}

// (5) 输出每门课程成绩最高的同学的基本信息
void print_top_students(struct Student stu[], int n) {
    int max_c_idx = 0, max_m_idx = 0, max_a_idx = 0;
    
    // 找出各科最高分的索引
    for (int i = 1; i < n; i++) {
        if (stu[i].score_c > stu[max_c_idx].score_c) max_c_idx = i;
        if (stu[i].score_math > stu[max_m_idx].score_math) max_m_idx = i;
        if (stu[i].score_algebra > stu[max_a_idx].score_algebra) max_a_idx = i;
    }
    
    printf("\n--- 各科单科状元基本信息 ---\n");
    printf("[C语言最高分]: %s (%s), 成绩: %.2f\n", stu[max_c_idx].name, stu[max_c_idx].id, stu[max_c_idx].score_c);
    printf("[高等数学最高分]: %s (%s), 成绩: %.2f\n", stu[max_m_idx].name, stu[max_m_idx].id, stu[max_m_idx].score_math);
    printf("[线性代数最高分]: %s (%s), 成绩: %.2f\n", stu[max_a_idx].name, stu[max_a_idx].id, stu[max_a_idx].score_algebra);
}

int main() {
    struct Student students[N];
    
    input_students(students, N);
    calc_average(students, N);
    sort_students(students, N);
    print_students(students, N);
    print_top_students(students, N);
    
    return 0;
}