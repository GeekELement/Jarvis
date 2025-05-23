import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class LLMAgent:
    def __init__(self):
        self.api_url = "https://api.example.com/v1/chat/completions"  # 示例 API 地址
        self.api_key = "your-api-key-here"  # 请替换为你的 API 密钥
        self.email_config = {
            "smtp_server": "smtp.example.com",  # 示例 SMTP 服务器
            "smtp_port": 587,  # 示例 SMTP 端口
            "sender": "your-email@example.com",  # 发送者邮箱
            "password": "your-email-password",  # 邮箱密码或授权码
            "receiver": "recipient@example.com"  # 接收者邮箱
        }

    def analyze_memo(self, content):
        try:
            prompt = f"""
            请分析以下备忘录内容，生成一个待办事项列表，包含优先级（高、中、低）：
            {content}
            
            请以 JSON 格式返回，格式如下：
            {{
                "tasks": [
                    {{"content": "任务内容", "priority": "high/medium/low"}}
                ]
            }}
            """
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-ai/DeepSeek-R1",  # 使用成功的模型名称
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1024,
                "response_format": {"type": "text"}
            }
            
            print("正在调用 API...")
            response = requests.post(self.api_url, headers=headers, json=data)
            print(f"API 响应状态码: {response.status_code}")
            print(f"API 响应内容: {response.text}")
            response.raise_for_status()
            
            # 解析响应并提取任务列表
            result = response.json()
            assistant_response = result['choices'][0]['message']['content']
            
            # 提取 JSON 字符串（去除 Markdown 格式）
            json_str = assistant_response.strip().replace('```json', '').replace('```', '').strip()
            
            # 确保响应是有效的 JSON
            try:
                tasks = json.loads(json_str)
                if not isinstance(tasks, dict) or "tasks" not in tasks:
                    raise ValueError("响应格式不正确")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"响应解析失败: {str(e)}")
                tasks = {"tasks": []}
            
            # 保存任务列表
            self.save_todo(tasks)
            print(f"保存的任务列表: {json.dumps(tasks, ensure_ascii=False, indent=2)}")
            
            # 只有在成功解析任务后才发送邮件
            if tasks and tasks.get("tasks"):
                self.send_email_notification(tasks)
            
            return tasks
            
        except Exception as e:
            print(f"API 调用失败: {str(e)}")
            return {"tasks": []}

    def save_todo(self, tasks):
        with open("data/todo.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

    def send_email_notification(self, tasks):
        try:
            # 构建邮件内容
            content = "新的待办事项列表：\n\n"
            for task in tasks["tasks"]:
                priority_map = {"high": "高", "medium": "中", "low": "低"}
                priority = priority_map.get(task["priority"], task["priority"])
                content += f"- [{priority}] {task['content']}\n"

            msg = MIMEText(content, 'plain', 'utf-8')
            msg['Subject'] = Header('新的待办事项提醒', 'utf-8')
            msg['From'] = self.email_config["sender"]
            msg['To'] = self.email_config["receiver"]

            # 使用 SSL 连接发送邮件
            with smtplib.SMTP_SSL(self.email_config["smtp_server"], self.email_config["smtp_port"]) as server:
                server.login(self.email_config["sender"], self.email_config["password"])
                server.sendmail(
                    self.email_config["sender"],
                    [self.email_config["receiver"]],
                    msg.as_string()
                )
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")