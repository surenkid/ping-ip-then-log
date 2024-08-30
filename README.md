# 多IP地址Ping监控记录工具

这是一个简单的Python工具,用于定期测试多个IP地址的连通性并记录结果。

## 功能特点

- 自动ping多个IP地址
- 定期执行测试
- 将结果保存到日志文件
- 简单的配置文件管理

## 安装

1. 克隆此仓库:
   ```bash
   git clone https://github.com/surenkid/ping-ip-then-log.git
   ```
2. 进入项目目录:
   ```bash
   cd ping-ip-then-log
   ```

## 使用方法

1. 在程序目录创建`config.txt`配置文件，输入要测试的IP地址,每行一个（格式见下文）
2. 运行`main.py`文件:
   ```bash
   python main.py
   ```
3. 程序会定期ping这些IP地址,并将结果记录到`log`目录中

## 配置文件

`config.txt`文件格式:
- 每行输入一个要测试的IP地址
- 示例:
  ```bash
  192.168.1.1
  8.8.8.8
  ```

## 日志文件

`log`目录下会生成以IP地址和当前日期命名的文件，记录每次ping的结果，包括时间戳、IP地址和延迟时间。

## 注意事项
- 如果ping失败,会记录失败原因
- 日志文件会以IP地址和当前日期命名，如`8.8.8.8-2024-07-25.txt`

## 注意事项

- 确保`config.txt`中的IP地址格式正确
- 程序会持续运行并定期执行ping测试,可以通过`Ctrl+C`来停止程序

## 故障排除

- 如果程序无法运行,请确保您的系统已安装Python和所需的依赖库
- 如遇到权限问题,请尝试以管理员身份运行程序

## 贡献

欢迎提交问题和拉取请求。对于重大更改,请先开issue讨论您想要改变的内容。