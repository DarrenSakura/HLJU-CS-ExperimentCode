#include <stdio.h>
#include <math.h>

int main() {
    double a, b, c, p, area;
    
    printf("请输入三角形的三条边长 (用空格分隔): ");
    scanf("%lf %lf %lf", &a, &b, &c);
    
    // 判断是否能构成三角形
    if (a + b > c && a + c > b && b + c > a) {
        p = (a + b + c) / 2.0; // 半周长
        area = sqrt(p * (p - a) * (p - b) * (p - c)); // 海伦公式
        printf("该三角形的面积为: %.2lf\n", area);
    } else {
        printf("输入的边长无法构成三角形！\n");
    }
    
    return 0;
}