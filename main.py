import threading
import time
import os
from ping3 import ping
from datetime import datetime
import re
import sys

# 从配置文件中读取IP地址
def read_ips_from_config(file_path='config.txt'):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"配置文件 '{file_path}' 不存在")
        
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
        
        if not lines:
            raise ValueError("配置文件为空，请添加至少一个IP地址")
        
        ips = []
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not ip_pattern.match(line):
                raise ValueError(f"第{i}行的IP地址格式不正确：'{line}'")
            
            # 验证IP地址的每个部分是否在0-255范围内
            parts = line.split('.')
            if not all(0 <= int(part) <= 255 for part in parts):
                raise ValueError(f"第{i}行的IP地址不合法：'{line}'")
            
            ips.append(line)
        
        return ips
    except FileNotFoundError as e:
        print(f"错误：{e}")
        print("请创建config.txt文件，并在其中每行添加一个有效的IP地址。")
    except ValueError as e:
        print(f"错误：{e}")
        print("请确保config.txt文件中每行包含一个有效的IP地址。")
    except Exception as e:
        print(f"读取配置文件时发生未知错误：{e}")
    
    return []

# 记录ping结果到日志文件
def log_ping_result(ip, log_file, ping_counts):
    while True:
        try:
            response_time = ping(ip, timeout=2)  # 设置超时时间为2秒
            if response_time is None or response_time is False:
                result = f"{datetime.now()}: {ip} 请求超时或无法到达"
            else:
                result = f"{datetime.now()}: {ip} 响应时间 {response_time * 1000:.2f} ms"
        except Exception as e:
            result = f"{datetime.now()}: {ip} 发生错误: {str(e)}"
        
        with open(log_file, 'a') as f:
            f.write(result + "\n")
        time.sleep(1)  # 等待1秒再ping
        ping_counts[ip] += 1  # 更新ping次数

# 创建日志文件路径
def create_log_file_path(ip):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, f"{ip}_{timestamp}.log")

# 主函数
def main():
    # 显示程序名和作者信息
    print("+" + "-" * 32 + "+")
    print("|" + " " * 32 + "|")
    print("|   多IP地址Ping测试记录工具   |")
    print("|      作者: surenkid        |")
    print("|" + " " * 32 + "|")
    print("+" + "-" * 32 + "+")
    print("\n")

    ips = read_ips_from_config()
    if not ips:
        print("配置文件格式不正确或为空。请按照正确格式编辑config.txt文件。")
        print("每行应包含一个有效的IP地址。")
        input("按任意键退出...")
        sys.exit(1)

    threads = []
    ping_counts = {ip: 0 for ip in ips}

    print(f"正在ping以下IP地址：{', '.join(ips)}")
    print("按Ctrl+C终止程序")

    for ip in ips:
        log_file = create_log_file_path(ip)
        thread = threading.Thread(target=log_ping_result, args=(ip, log_file, ping_counts))
        thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        threads.append(thread)
        thread.start()

    try:
        while True:
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
            print(f"正在ping以下IP地址：{', '.join(ips)}")
            for ip, count in ping_counts.items():
                print(f"{ip}: 已ping {count}次")
            print("\n按Ctrl+C终止程序")
    except KeyboardInterrupt:
        print("\n程序终止，日志已保存到logs文件夹中，正在退出...")

if __name__ == "__main__":
    main()
