import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os

# 1. 设计爬虫类结构
class SimpleWebCrawler:
    def __init__(self):
        # 设置请求头，模拟普通浏览器访问，防止被简单的反爬虫机制拦截
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    # 2. 实现URL验证和过滤
    def is_valid_url(self, url):
        """验证 URL 是否合法且为 HTTP/HTTPS 协议"""
        try:
            result = urllib.parse.urlparse(url)
            # 检查是否包含协议（scheme）和域名（netloc）
            return all([result.scheme in ['http', 'https'], result.netloc])
        except ValueError:
            return False

    def fetch_page(self, url):
        """发送 HTTP 请求获取网页 HTML 内容"""
        if not self.is_valid_url(url):
            print(f"错误：无效的 URL 格式 -> {url}")
            return None

        print(f"正在获取网页内容: {url} ...")
        try:
            # 掌握HTTP请求基础：使用 requests 发送 GET 请求
            response = requests.get(url, headers=self.headers, timeout=10)
            # 检查响应状态码，如果不是 200 则抛出异常
            response.raise_for_status()
            # 解决可能出现的中文乱码问题
            response.encoding = response.apparent_encoding 
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"网络请求失败: {e}")
            return None

    # 3. 完成网页解析功能
    def parse_html(self, html_content, base_url):
        """解析 HTML，提取标题、文章标题(h1,h2)和前几个超链接"""
        print("正在解析网页内容...")
        # 学习HTML解析技术：使用 BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        result = {
            'page_title': '',
            'headings': [],
            'links': []
        }

        # 提取网页 <title>
        if soup.title and soup.title.string:
            result['page_title'] = soup.title.string.strip()

        # 提取页面中的 <h1> 和 <h2> 标签文本
        for tag in soup.find_all(['h1', 'h2']):
            text = tag.get_text(strip=True)
            if text:
                result['headings'].append(text)

        # 提取页面中的超链接 (<a> 标签的 href 属性)，限制提取前 10 个有效链接
        link_count = 0
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # 将相对路径转换为绝对路径
            full_url = urllib.parse.urljoin(base_url, href)
            # 简单过滤：只保留 http/https 链接
            if full_url.startswith('http'):
                result['links'].append(full_url)
                link_count += 1
            if link_count >= 10:
                break

        return result

    # 4. 添加结果保存功能
    def save_results(self, data, filename="crawler_results.json"):
        """将解析到的数据保存为 JSON 文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"结果已成功保存至文件: {os.path.abspath(filename)}")
        except Exception as e:
            print(f"保存文件时发生错误: {e}")

    def run(self, url):
        """运行爬虫主流程"""
        html = self.fetch_page(url)
        if html:
            data = self.parse_html(html, base_url=url)
            
            # 在控制台打印摘要信息
            print("\n--- 提取结果摘要 ---")
            print(f"网页标题: {data['page_title']}")
            print(f"提取到 {len(data['headings'])} 个标题 (H1/H2)")
            print(f"提取到 {len(data['links'])} 个有效链接")
            print("-" * 20)
            
            # 保存到文件
            self.save_results(data)

def main():
    crawler = SimpleWebCrawler()
    
    # 5. 测试不同网站
    print("=== 简易网络爬虫 ===")
    print("内置测试网站：")
    print("1. 百度首页 (https://www.baidu.com)")
    print("2. 豆瓣电影 (https://movie.douban.com)")
    print("3. 输入自定义网址")
    print("4. 退出")

    while True:
        choice = input("\n请选择操作 (1-4): ")
        
        url = ""
        if choice == '1':
            url = "https://www.baidu.com"
        elif choice == '2':
            url = "https://movie.douban.com"
        elif choice == '3':
            url = input("请输入完整的网址 (如 https://www.example.com): ").strip()
        elif choice == '4':
            print("退出爬虫程序，再见！")
            break
        else:
            print("无效的选择，请重新输入！")
            continue

        if url:
            crawler.run(url)

if __name__ == "__main__":
    main()