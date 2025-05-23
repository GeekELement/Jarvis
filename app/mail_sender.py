import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import yaml

class MailSender:
    def __init__(self):
        load_dotenv()
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = self.config["email"]["smtp_server"]
        self.smtp_port = self.config["email"]["smtp_port"]
        self.recipient = self.config["email"]["recipient"]

    def format_todo_list(self, tasks: dict) -> str:
        html = "<h2>Your Daily Todo List</h2><ul>"
        for task in tasks["tasks"]:
            html += f"""
            <li>
                <strong>Date:</strong> {task['date']}<br>
                <strong>Task:</strong> {task['task']}<br>
                <strong>Priority:</strong> {task['priority']}
            </li>
            """
        html += "</ul>"
        return html

    def send_todo_list(self, tasks: dict):
        msg = MIMEMultipart()
        msg["From"] = self.email_user
        msg["To"] = self.recipient
        msg["Subject"] = "Daily Todo List"

        html_content = self.format_todo_list(tasks)
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)