import string
import os
from collections import Counter

# 1. 创建WordFrequencyAnalyzer类
class WordFrequencyAnalyzer:
    def __init__(self):
        self.word_counts = {}

    # 3. 添加文件读取方法
    def read_file(self, file_path):
        """读取指定路径的文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"错误：找不到文件 '{file_path}'。请检查路径是否正确。")
            return None
        except Exception as e:
            print(f"读取文件时发生错误：{e}")
            return None

    # 2. 实现文本清理功能
    def clean_text(self, text):
        """清洗文本：转小写并去除标点符号"""
        # 将文��转换为小写
        text = text.lower()
        # 替换所有标点符号为空格（保留单词的独立性）
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        cleaned_text = text.translate(translator)
        return cleaned_text

    # 4. 实现词频统计逻辑
    def analyze(self, file_path):
        """分析文件的词频"""
        text = self.read_file(file_path)
        if text is None:
            return False

        # 清洗数据
        cleaned_text = self.clean_text(text)
        
        # 分割字符串为单词列表
        words = cleaned_text.split()
        
        # 使用字典数据结构（这里使用 collections.Counter 优化）统计词频
        self.word_counts = Counter(words)
        return True

    def get_top_words(self, n=10):
        """获取出现频率最高的前 n 个单词"""
        if not self.word_counts:
            return []
        return self.word_counts.most_common(n)

# 5. 设计用户交互界面
def main():
    # 自动创建一个测试文件，方便实验直接运行
    sample_file = "sample_text.txt"
    if not os.path.exists(sample_file):
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write("Hello world! This is a test file for the Word Frequency Analyzer. "
                    "Python is great, and learning Python is fun. Let's write some Python code!")

    analyzer = WordFrequencyAnalyzer()
    
    while True:
        print("\n=== 词频统计器 ===")
        print("1. 分析文件词频")
        print("2. 退出")
        choice = input("请选择操作 (1/2): ")
        
        if choice == '2':
            print("退出程序，再见！")
            break
            
        elif choice == '1':
            file_path = input(f"请输入要分析的文件路径 (直接回车将使用默认测试文件 '{sample_file}'): ")
            if not file_path.strip():
                file_path = sample_file
            
            if analyzer.analyze(file_path):
                try:
                    n_str = input("请输入要查看出现频率最高的前几个单词 (默认查看前 10 个，直接回车): ")
                    n = int(n_str) if n_str.strip() else 10
                    
                    top_words = analyzer.get_top_words(n)
                    
                    print(f"\n--- '{file_path}' 的词频统计结果 (前 {n} 个) ---")
                    print(f"{'单词':<15} | {'出现次数':<5}")
                    print("-" * 30)
                    for word, count in top_words:
                        print(f"{word:<15} | {count:<5}")
                except ValueError:
                    print("错误：请输入有效的数字！")
        else:
            print("无效的选择，请重新输入！")

if __name__ == "__main__":
    main()