#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <queue>
#include <iomanip>
#include <cstdlib>
#include <ctime>

using namespace std;

// 进程状态枚举
enum State {
    READY,
    RUN_CPU,
    RUN_IO,
    WAITING,
    DONE
};

// 进程控制块 PCB
struct PCB {
    int pid;
    string name;
    State state;
    vector<string> instructions;
    int pc;             // 程序计数器（当前执行到第几条指令）
    int wait_timer;     // I/O 等待计时器
    
    PCB(int id) : pid(id), state(READY), pc(0), wait_timer(0) {
        name = "P" + to_string(id);
    }
};

// 任务1：生成随机的程序文件
void generatePrograms(int k, int percent, int min_inst, int max_inst) {
    srand(time(NULL));
    cout << "--- 正在生成 " << k << " 个程序文件 ---" << endl;
    for (int i = 0; i < k; ++i) {
        string filename = "P" + to_string(i) + ".txt";
        ofstream outFile(filename);
        int num_inst = min_inst + rand() % (max_inst - min_inst + 1);
        
        for (int j = 0; j < num_inst; ++j) {
            int r = rand() % 100 + 1;
            if (r <= percent) {
                outFile << "cpu\n";
            } else {
                outFile << "io\n";
            }
        }
        outFile.close();
        cout << "生成文件 " << filename << "，包含 " << num_inst << " 条指令。" << endl;
    }
    cout << "-----------------------------------" << endl << endl;
}

// 获取状态对应的字符串输出
string getStateString(State state) {
    switch (state) {
        case READY: return "READY";
        case RUN_CPU: return "RUN:cpu";
        case RUN_IO: return "RUN:io";
        case WAITING: return "WAITING";
        case DONE: return "DONE";
        default: return "";
    }
}

// 任务2：模拟操作系统进程调度
void simulate(int k) {
    vector<PCB> processes;
    queue<int> ready_queue;
    
    // 读入文件并初始化进程
    for (int i = 0; i < k; ++i) {
        PCB pcb(i);
        string filename = "P" + to_string(i) + ".txt";
        ifstream inFile(filename);
        string inst;
        while (inFile >> inst) {
            pcb.instructions.push_back(inst);
        }
        inFile.close();
        processes.push_back(pcb);
        ready_queue.push(i);
    }

    int time = 1;
    int cpu_busy_time = 0;
    int io_busy_time = 0;
    int running_pid = -1;
    
    // 打印表头
    cout << left << setw(6) << "Time";
    for (int i = 0; i < k; ++i) {
        cout << setw(12) << ("PID:" + to_string(i));
    }
    cout << setw(6) << "CPU" << "IOs" << endl;

    bool all_done = false;

    while (!all_done) {
        bool cpu_busy = false;
        int active_ios = 0;
        bool state_changed = false; // 用于标记是否有进程状态发生改变（对应输出中的*号）

        // 1. 更新处于 WAITING 状态的进程
        for (int i = 0; i < k; ++i) {
            if (processes[i].state == WAITING) {
                processes[i].wait_timer--;
                active_ios++;
                if (processes[i].wait_timer == 0) {
                    processes[i].pc++; // 该io指令彻底执行完毕
                    if (processes[i].pc >= processes[i].instructions.size()) {
                        processes[i].state = DONE;
                    } else {
                        processes[i].state = READY;
                        ready_queue.push(i);
                    }
                    state_changed = true;
                }
            }
        }

        // 2. 处理当前运行的进程
        if (running_pid != -1) {
            PCB& cur_p = processes[running_pid];
            if (cur_p.state == RUN_CPU) {
                cur_p.pc++;
                if (cur_p.pc >= cur_p.instructions.size()) {
                    cur_p.state = DONE;
                    running_pid = -1;
                } else {
                    // ���抢占式，继续运行下一条指令
                    if (cur_p.instructions[cur_p.pc] == "cpu") {
                        cur_p.state = RUN_CPU;
                    } else {
                        cur_p.state = RUN_IO;
                    }
                }
            } else if (cur_p.state == RUN_IO) {
                // RUN:io ��用了1个时间片的CPU，接下来进入 WAITING 4个时间片
                cur_p.state = WAITING;
                cur_p.wait_timer = 4;
                running_pid = -1;
            }
        }

        // 3. 调度新的进程（如果CPU空闲）
        if (running_pid == -1 && !ready_queue.empty()) {
            running_pid = ready_queue.front();
            ready_queue.pop();
            PCB& cur_p = processes[running_pid];
            
            if (cur_p.instructions[cur_p.pc] == "cpu") {
                cur_p.state = RUN_CPU;
            } else {
                cur_p.state = RUN_IO;
            }
        }

        // 统计 CPU 和 IO 忙碌状态
        if (running_pid != -1) {
            cpu_busy = true;
            cpu_busy_time++;
        }
        if (active_ios > 0) {
            io_busy_time++;
        }

        // 4. 打印当前时刻状态
        string time_str = to_string(time) + (state_changed ? "*" : "");
        cout << left << setw(6) << time_str;
        
        all_done = true;
        for (int i = 0; i < k; ++i) {
            cout << setw(12) << getStateString(processes[i].state);
            if (processes[i].state != DONE) {
                all_done = false;
            }
        }
        
        cout << setw(6) << (cpu_busy ? "1" : "");
        cout << (active_ios > 0 ? to_string(active_ios) : "") << endl;

        if (all_done) break;
        time++;
    }

    // 打印统计结果
    cout << "\nStats: Total Time " << time << endl;
    cout << fixed << setprecision(2);
    cout << "Stats: CPU Busy " << cpu_busy_time << " (" << (double)cpu_busy_time / time * 100 << "%)" << endl;
    cout << "Stats: IO Busy  " << io_busy_time << " (" << (double)io_busy_time / time * 100 << "%)" << endl;
}

int main() {
    int k, percent, min_inst, max_inst;
    
    cout << "请输入参数 (程序个数k, CPU指令占比percent, 最小指令数min, 最大指令数max):" << endl;
    // 示例输入: 6 80 5 10
    if (cin >> k >> percent >> min_inst >> max_inst) {
        generatePrograms(k, percent, min_inst, max_inst);
        simulate(k);
    } else {
        cout << "输入错误！" << endl;
    }

    return 0;
}