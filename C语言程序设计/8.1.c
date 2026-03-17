#include <stdio.h>

// (1) 录入学号和成绩
void input_data(int ids[], float scores[][3], int n) {
    printf("--- 开始录入 %d 个学生的信息 ---\n", n);
    for (int i = 0; i < n; i++) {
        printf("请输入第 %d 个学生的学号: ", i + 1);
        scanf("%d", &ids[i]);
        printf("请输入该学生的3门课成绩(用空格分隔): ");
        scanf("%f %f %f", &scores[i][0], &scores[i][1], &scores[i][2]);
    }
    printf("录入完成！\n");
}

// (2) 求第一门课的平均分
void calc_first_course_avg(float scores[][3], int n) {
    float sum = 0;
    for (int i = 0; i < n; i++) {
        sum += scores[i][0];
    }
    printf("第一门课的平均分为: %.2f\n", sum / n);
}

// (3) 找出有2门以上课程不及格的学生
void find_failed_students(int ids[], float scores[][3], int n) {
    int found = 0;
    printf("--- 有2门以上不及格的学生信息 ---\n");
    for (int i = 0; i < n; i++) {
        int fail_count = 0;
        float sum = 0;
        for (int j = 0; j < 3; j++) {
            if (scores[i][j] < 60.0) {
                fail_count++;
            }
            sum += scores[i][j];
        }
        
        if (fail_count >= 2) {
            found = 1;
            printf("学号: %d | 成绩: %.1f, %.1f, %.1f | 平均分: %.2f\n", 
                   ids[i], scores[i][0], scores[i][1], scores[i][2], sum / 3.0);
        }
    }
    if (!found) {
        printf("没有符合条件的学生。\n");
    }
}

// (4) 找出平均成绩90分以上或全部课成绩在85分以上的学生
void find_excellent_students(int ids[], float scores[][3], int n) {
    int found = 0;
    printf("--- 优秀学生名单(平均分>=90 或 全部课程>=85) ---\n");
    for (int i = 0; i < n; i++) {
        float sum = 0;
        int all_above_85 = 1; // 假设全部大于等于85
        
        for (int j = 0; j < 3; j++) {
            sum += scores[i][j];
            if (scores[i][j] < 85.0) {
                all_above_85 = 0; // 只要有一门小于85，标志位置0
            }
        }
        
        float avg = sum / 3.0;
        if (avg >= 90.0 || all_above_85) {
            found = 1;
            printf("学号: %d | 平均分: %.2f\n", ids[i], avg);
        }
    }
    if (!found) {
        printf("没有符合条件的学生。\n");
    }
}

int main() {
    int ids[5] = {0};
    float scores[5][3] = {0};
    int choice;
    int is_input_done = 0; // 标记是否已经录入过数据

    while (1) {
        printf("\n****************************************************************\n");
        printf("（1）录入每个学生的学号和成绩；\n");
        printf("（2）求第一门课的平均分；\n");
        printf("（3）找出有2门以上课程不及格的学生；\n");
        printf("（4）找出平均成绩90分以上或全部课成绩在85分以上的学生；\n");
        printf("（0）退出系统。\n");
        printf("****************************************************************\n");
        printf("请选择操作 (0-4): ");
        scanf("%d", &choice);

        // 如果没有录入数据且选了 2/3/4，提示先录入
        if (choice >= 2 && choice <= 4 && !is_input_done) {
            printf("提示：请先执行操作 (1) 录入学生数据！\n");
            continue;
        }

        switch (choice) {
            case 1:
                input_data(ids, scores, 5);
                is_input_done = 1;
                break;
            case 2:
                calc_first_course_avg(scores, 5);
                break;
            case 3:
                find_failed_students(ids, scores, 5);
                break;
            case 4:
                find_excellent_students(ids, scores, 5);
                break;
            case 0:
                printf("退出系统。再见！\n");
                return 0;
            default:
                printf("无效输入，请重新选择。\n");
        }
    }
    return 0;
}