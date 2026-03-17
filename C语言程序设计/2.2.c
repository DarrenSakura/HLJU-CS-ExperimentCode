#include <stdio.h>
#include <math.h>

int main() {
    double a, b, c, delta;
    double p, q;
    
    printf("请输入一元二次方程的系数 a, b, c（a≠0，用空格分隔）: ");
    scanf("%lf %lf %lf", &a, &b, &c);
    
    if (a == 0) {
        printf("系数 a 不能为 0，这不是一元二次方程。\n");
    } else {
        delta = b * b - 4 * a * c;
        p = -b / (2.0 * a); // 实部或相等的根
        
        if (delta > 0) {
            q = sqrt(delta) / (2.0 * a);
            printf("方程有两个不相等的实数根: x1 = %.2lf, x2 = %.2lf\n", p + q, p - q);
        } else if (delta == 0) {
            printf("方程有两个相等的实数根: x1 = x2 = %.2lf\n", p);
        } else {
            // 当 delta < 0 时，求复数根
            q = sqrt(-delta) / (2.0 * a);
            printf("方程有两个共轭复数根: x1 = %.2lf+%.2lfi, x2 = %.2lf-%.2lfi\n", p, q, p, q);
        }
    }
    
    return 0;
}