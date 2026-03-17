import re
import os
from collections import Counter

# 1. 设计日志解析器类
class LogAnalyzer:
    def __init__(self):
        self.parsed_logs = []
        
        # 2. 实现多种日志格式支持（预定义正则表达式模式）
        # 格式A: 简化的 Nginx/Apache 访问日志格式
        # 示例: 192.168.1.1 - - [17/Mar/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024
        self.web_log_pattern = re.compile(
            r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - - \[(?P<timestamp>.*?)\] '
            r'"(?P<method>[A-Z]+) (?P<url>.*?) HTTP/.*?" (?P<status>\d{3}) (?P<size>\d+)'
        )
        
        # 格式B: 标准的应用程序运行日志格式
        # 示例: [2026-03-17 10:05:00] [ERROR] Database connection failed.
        self.app_log_pattern = re.compile(
            r'\[(?P<timestamp>.*?)\] \[(?P<level>[A-Z]+)\] (?P<message>.*)'
        )

    def load_and_parse(self, file_path, log_type):
        """读取文件并根据指定类型使用正则匹配进行解析"""
        self.parsed_logs = []
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return False

        pattern = self.web_log_pattern if log_type == 'web' else self.app_log_pattern
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = pattern.match(line.strip())
                if match:
                    # 将正则匹配到的命名组直接转换为字典并保存
                    self.parsed_logs.append(match.groupdict())
                else:
                    # 记录解析失败的行（可用于发现未知格式）
                    print(f"警告：无法解析日志行 -> {line.strip()}")
        
        print(f"成功解析 {len(self.parsed_logs)} 条日志。")
        return True

    # 3. 完成统计分析功能 (基础数据分析)
    def analyze_web_logs(self):
        """分析Web日志：统计IP访问量和HTTP状态码"""
        if not self.parsed_logs or 'ip' not in self.parsed_logs[0]:
            print("当前没有解析Web日志或日志格式不对。")
            return

        ip_counter = Counter(log['ip'] for log in self.parsed_logs)
        status_counter = Counter(log['status'] for log in self.parsed_logs)

        print("\n--- Web日志统计分析 ---")
        print("访问量前 3 的 IP 地址:")
        for ip, count in ip_counter.most_common(3):
            print(f"  {ip}: {count} 次")
            
        print("\nHTTP 状态码统计 (用于异常检测):")
        for status, count in status_counter.items():
            # 简单异常检测：4xx 和 5xx 状态码为异常
            note = " (异常/错误!)" if status.startswith('4') or status.startswith('5') else " (正常)"
            print(f"  {status}: {count} 次{note}")

    def analyze_app_logs(self):
        """分析App日志：统计各日志级别的数量"""
        if not self.parsed_logs or 'level' not in self.parsed_logs[0]:
            print("当前没有解析App日志或日志格式不对。")
            return

        level_counter = Counter(log['level'] for log in self.parsed_logs)
        
        print("\n--- App日志统计分析 ---")
        print("日志级别分布:")
        for level, count in level_counter.items():
            print(f"  {level}: {count} 条")

    # 4. 添加搜索和报告功能
    def search_logs(self, keyword):
        """根据关键字全文搜索已解析的日志内容"""
        print(f"\n--- 搜索结果 (关键字: '{keyword}') ---")
        found = False
        for log in self.parsed_logs:
            # 将字典的所有 value 拼接成字符串进行搜索
            if keyword.lower() in str(log.values()).lower():
                print(log)
                found = True
        if not found:
            print("未找到匹配的日志。")

def generate_test_logs():
    """5. 测试不同日志文件：自动生成测试用的日志文件"""
    web_log_file = "test_web.log"
    if not os.path.exists(web_log_file):
        with open(web_log_file, "w") as f:
            f.write('192.168.1.10 - - [17/Mar/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024\n')
            f.write('192.168.1.10 - - [17/Mar/2026:10:00:05 +0000] "GET /style.css HTTP/1.1" 200 512\n')
            f.write('10.0.0.5 - - [17/Mar/2026:10:01:00 +0000] "POST /login HTTP/1.1" 401 128\n')
            f.write('192.168.1.11 - - [17/Mar/2026:10:02:15 +0000] "GET /admin HTTP/1.1" 403 256\n')
            f.write('10.0.0.5 - - [17/Mar/2026:10:03:00 +0000] "GET /api/data HTTP/1.1" 500 0\n')

    app_log_file = "test_app.log"
    if not os.path.exists(app_log_file):
        with open(app_log_file, "w") as f:
            f.write('[2026-03-17 10:00:00] [INFO] Application started successfully.\n')
            f.write('[2026-03-17 10:05:12] [WARNING] Memory usage is above 80%.\n')
            f.write('[2026-03-17 10:15:30] [ERROR] Database connection timeout.\n')
            f.write('[2026-03-17 10:16:00] [INFO] Retrying database connection...\n')

    return web_log_file, app_log_file

def main():
    web_file, app_file = generate_test_logs()
    analyzer = LogAnalyzer()

    while True:
        print("\n=== 日志分析器 ===")
        print(f"1. 分析 Web 访问日志 (使用自动生成的 {web_file})")
        print(f"2. 分析 App 运行日志 (使用自动生成的 {app_file})")
        print("3. 在当前加载的日志中搜索")
        print("4. 退出")
        
        choice = input("请选择操作 (1-4): ")
        
        if choice == '1':
            if analyzer.load_and_parse(web_file, 'web'):
                analyzer.analyze_web_logs()
        elif choice == '2':
            if analyzer.load_and_parse(app_file, 'app'):
                analyzer.analyze_app_logs()
        elif choice == '3':
            if not analyzer.parsed_logs:
                print("请先选择 1 或 2 加载并解析日志文件！")
            else:
                keyword = input("请输入要搜索的关键字 (如 IP、状态码、错误信息等): ")
                analyzer.search_logs(keyword)
        elif choice == '4':
            print("退出系统，再见！")
            break
        else:
            print("无效输入，请重新选择。")

if __name__ == "__main__":
    main()