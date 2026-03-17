#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <iomanip>
using namespace std;
// --- 算法参数设置 ---
const int POPULATION_SIZE = 100;    // 种群大小
const int CHROMOSOME_LENGTH = 20;   // 染色体长度 (决定解的精度)
const double CROSSOVER_RATE = 0.7;  // 交叉概率
const double MUTATION_RATE = 0.01;  // 变异概率
const int MAX_GENERATIONS = 200;    // 最大迭代次数
// --- 问题定义 ---
const double X_MIN = -1.0;          // 定义域下界
const double X_MAX = 2.0;           // 定义域上界
// 目标函数: f(x) = x * sin(10*pi*x) + 2.0
double target_function(double x) {
    return x * sin(10 * 3.1415926535 * x) + 2.0;
}
// 个体结构体
struct Individual {
    string chromosome; // 二进制染色体
    double fitness;    // 适应度
    double value;      // 对应的实数x值
};
// 工具函数：生成随机0-1浮点数
double random_double() {
    return (double)rand() / RAND_MAX;
}
// 工具函数：生成随机整数 [min, max]
int random_int(int min, int max) {
    return min + rand() % (max - min + 1);
}
// 解码：二进制串 -> 实数
double decode(const string& chromosome) {
    long decimal_value = 0;
    long power_of_two = 1;
    for (int i = chromosome.length() - 1; i >= 0; --i) {
        if (chromosome[i] == '1') {
            decimal_value += power_of_two;
        }
        power_of_two *= 2;
    }
    // 映射公式: x = min + decimal * (max - min) / (2^L - 1)
    return X_MIN + (double)decimal_value * (X_MAX - X_MIN) / (pow(2, CHROMOSOME_LENGTH) - 1);
}
// 初始化种群
vector<Individual> initialize_population() {
    vector<Individual> population(POPULATION_SIZE);
    for (int i = 0; i < POPULATION_SIZE; ++i) {
        string chrom = "";
        for (int j = 0; j < CHROMOSOME_LENGTH; ++j) {
            chrom += (random_int(0, 1) ? '1' : '0');
        }
        population[i].chromosome = chrom;
        // 计算初始适应度
        population[i].value = decode(chrom);
        population[i].fitness = target_function(population[i].value);
    }
    return population;
}
// 选择（轮盘赌算法）
Individual select(const vector<Individual>& population) {
    double total_fitness = 0;
    for (const auto& ind : population) {
        // 假设适应度必须为正。如果函数可能有负值，需要进行平移处理
        // 这里函数 f(x) = x*sin(...) + 2.0 在 [-1,2] 范围内大约是 [0, 4]，基本安全
        // 为保险起见，如果fitness小于0，视为0处理（实际应用需根据具体函数调整）
        total_fitness += max(0.0, ind.fitness);
    }
    double slice = random_double() * total_fitness;
    double current_sum = 0;
    for (const auto& ind : population) {
        current_sum += max(0.0, ind.fitness);
        if (current_sum >= slice) {
            return ind;
        }
    }
    return population.back(); // 默认返回最后一个
}
// 交叉
void crossover(Individual& p1, Individual& p2) {
    if (random_double() < CROSSOVER_RATE) {
        int point = random_int(1, CHROMOSOME_LENGTH - 1);
        string c1 = p1.chromosome.substr(0, point) + p2.chromosome.substr(point);
        string c2 = p2.chromosome.substr(0, point) + p1.chromosome.substr(point);
        p1.chromosome = c1;
        p2.chromosome = c2;
    }
}
// 变异
void mutate(Individual& ind) {
    for (int i = 0; i < CHROMOSOME_LENGTH; ++i) {
        if (random_double() < MUTATION_RATE) {
            ind.chromosome[i] = (ind.chromosome[i] == '0' ? '1' : '0');
        }
    }
}
// 更新个体的数值和适应度
void evaluate(Individual& ind) {
    ind.value = decode(ind.chromosome);
    ind.fitness = target_function(ind.value);
}
int main() {
    srand(time(0)); // 随机数种子
    // 1. 初始化
    vector<Individual> population = initialize_population();
    Individual best_global;
    best_global.fitness = -1e9; // 初始极小值
    cout << "开始遗传算法优化..." << endl;
    cout << "寻找 f(x) = x * sin(10*pi*x) + 2.0 的最大值" << endl;
    cout << "------------------------------------------------" << endl;
    // 2. 迭代进化
    for (int generation = 1; generation <= MAX_GENERATIONS; ++generation) {
        vector<Individual> new_population;
        // 精英保留策略：先把上一代最好的直接留下来，防止退化
        Individual best_current = population[0];
        for (const auto& ind : population) {
            if (ind.fitness > best_current.fitness) {
                best_current = ind;
            }
        }
        if (best_current.fitness > best_global.fitness) {
            best_global = best_current;
        }      
        // 可选：将最好的个体直接加入新种群
        // new_population.push_back(best_current); 
        // 生成新一代
        while (new_population.size() < POPULATION_SIZE) {
            // 选择
            Individual p1 = select(population);
            Individual p2 = select(population);
            // 交叉
            crossover(p1, p2);
            // 变异
            mutate(p1);
            mutate(p2);
            // 重新评估
            evaluate(p1);
            evaluate(p2);
            new_population.push_back(p1);
            if (new_population.size() < POPULATION_SIZE) new_population.push_back(p2);
        }
        population = new_population;
        // 输出部分代数的日志
        if (generation % 20 == 0 || generation == 1) {
            cout << "Generation " << setw(3) << generation 
                 << " | Best Fitness: " << fixed << setprecision(6) << best_global.fitness 
                 << " | x = " << best_global.value << endl;
        }
    }
    cout << "------------------------------------------------" << endl;
    cout << "最终结果:" << endl;
    cout << "最优 x 值: " << best_global.value << endl;
    cout << "最大函数值: " << best_global.fitness << endl;
    //cout << "对应的二进制串: " << best_global.chromosome << endl;
    return 0;
}