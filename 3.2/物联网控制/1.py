import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False  
class IncrementalPID:
    """增量式 PID 控制器"""
    def __init__(self, kp, ki, kd, output_limits=(None, None)):
        self.kp = kp #比例增益
        self.ki = ki #积分增益
        self.kd = kd #微分增益
        self.e_k1 = 0.0  # 上次误差
        self.e_k2 = 0.0  # 上上次误差
        self.output = 0.0  # 当前输出uk
        self.out_min, self.out_max = output_limits #上下限
    def update(self, target, current_feedback):
        e_k = target - current_feedback #当前误差=目标值-反馈值
        #增量式 PID 计算增量
        delta_u = (self.kp * (e_k - self.e_k1) + self.ki * e_k + self.kd * (e_k - 2 * self.e_k1 + self.e_k2))
        self.output += delta_u #输出=上次输出+增量
        #输出上下限
        if self.out_max is not None:
            self.output = min(self.output, self.out_max) 
        if self.out_min is not None:
            self.output = max(self.output, self.out_min) 
        self.e_k2 = self.e_k1 #更新上上次误差
        self.e_k1 = e_k #更新上次误差
        return self.output
class SimulationModel:
    """仿真模型：一阶惯性系统"""
    def __init__(self):
        self.state = 0.0 #初始0
    def update(self, control_input):
        self.state = 0.85 * self.state + 0.15 * control_input #85旧15新
        return self.state
def run_simulation():
    system = SimulationModel()
    pid = IncrementalPID(kp=0.6, ki=0.15, kd=0.1, output_limits=(0, 200)) #PID 参数和输出限制
    target_value = 100.0 #目标值
    simulation_steps = 200 #仿真步数
    history_state = []
    history_target = []
    history_control = []
    for step in range(simulation_steps):
        if step == simulation_steps * 0.5:  
            target_value = 150.0
        current_state = system.state
        control_signal = pid.update(target_value, current_state)
        system.update(control_signal)
        history_state.append(current_state)
        history_target.append(target_value)
        history_control.append(control_signal)
    plt.figure(figsize=(10, 6))
    # 上图：目标值与系统输出
    plt.subplot(2, 1, 1)
    plt.plot(history_target, "r--", label="目标值（设定值）")
    plt.plot(history_state, "b-", label="系统状态（输出）")
    plt.title("增量式 PID 控制仿真")
    plt.ylabel("系统状态")
    plt.legend()
    plt.grid(True)
    # 下图：控制量输出
    plt.subplot(2, 1, 2)
    plt.plot(history_control, "g-", label="控制量 u(k)")
    plt.xlabel("时间步（k）")
    plt.ylabel("控制输出")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    run_simulation()