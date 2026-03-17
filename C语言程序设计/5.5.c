#include <stdio.h>

#define N 3 // 学生数
#define M 4 // 课程数

int main() {
    float scores[N][M];
    float total_sum = 0;
    float max_score = -1;
    int max_stu = 0, max_course = 0;

    // 输入成绩
    for (int i = 0; i < N; i++) {
        printf("请输入第 %d 个学生的 %d 门成绩: ", i + 1, M);
        for (int j = 0; j < M; j++) {
            scanf("%f", &scores[i][j]);
            total_sum += scores[i][j];
            
            // (1) 找最高分
            if (scores[i][j] > max_score) {
                max_score = scores[i][j];
                max_stu = i;
                max_course = j;
            }
        }
    }

    printf("\n(1) 最高分是 %.1f, 属于第 %d 号学生, 第 %d 门课程。\n", max_score, max_stu + 1, max_course + 1);

    // (2) 找有不及格的学生
    printf("\n(2) 有不及格课程的学生及其全部成绩:\n");
    for (int i = 0; i < N; i++) {
        int fail = 0;
        for (int j = 0; j < M; j++) {
            if (scores[i][j] < 60) fail = 1;
        }
        if (fail) {
            printf("学生号 %d: ", i + 1);
            for (int j = 0; j < M; j++) printf("%.1f ", scores[i][j]);
            printf("\n");
        }
    }

    // (3) 总平均数
    printf("\n(3) 全部学生全部课程的总平均数: %.2f\n", total_sum / (N * M));

    return 0;
}