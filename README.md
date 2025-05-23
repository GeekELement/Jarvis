# Jarvis - 智能备助手与任务管理系统

Jarvis是一个基于FastAPI开发的智能备忘录和任务管理系统，它能够帮助用户管理日常备忘录，并通过AI分析自动生成待办任务。

## 功能特点

- 📝 备忘录管理：添加、删除和查看备忘录内容
- 🤖 AI分析：自动分析备忘录内容并生成待办任务
- 📅 定时任务：支持定时分析和邮件通知
- 📧 邮件通知：可配置邮件提醒功能
- 🎯 任务管理：查看和管理待办任务列表
- 💻 现代化界面：使用HTMX实现流畅的用户体验

## 技术栈

- FastAPI：后端Web框架
- HTMX：前端交互
- Jinja2：模板引擎
- Docker：容器化部署

## 安装说明

1. 克隆项目
```bash
git clone https://github.com/yourusername/Jarvis.git
cd Jarvis
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置
编辑 `config.yaml` 文件，设置：
- 分析时间
- 邮件通知时间
- SMTP服务器配置
- 接收通知的邮箱地址

## 使用方法

1. 启动服务
```bash
cd c:\Users\geeke\Desktop\Jarvis(这里填写你的项目路径)
uvicorn app.main:app --reload
```

2. 访问系统
打开浏览器访问 `http://localhost:8000`

3. 使用功能
- 在主页添加新的备忘录
- 查看和管理待办任务
- 使用AI分析功能自动生成任务
- 配置邮件通知

## 项目结构

```
Jarvis/
├── app/                # 应用主目录
│   ├── main.py        # 主程序
│   ├── llm_agent.py   # AI分析模块
│   ├── mail_sender.py # 邮件发送模块
│   └── scheduler.py   # 定时任务模块
├── data/              # 数据存储目录
├── static/            # 静态文件
├── templates/         # HTML模板
├── config.yaml        # 配置文件
└── Dockerfile         # Docker配置文件
```

## 配置说明

在 `config.yaml` 中可以配置以下内容：

```yaml
schedule:
  analyze_time: "08:00"    # 每日分析时间
  email_time: "08:10"      # 邮件发送时间
email:
  recipient: "your@email.com"  # 接收通知的邮箱
  smtp_server: "smtp.example.com"  # SMTP服务器
  smtp_port: 587           # SMTP端口
```

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。

## 许可证

MIT License 
