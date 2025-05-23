from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .llm_agent import LLMAgent
from .mail_sender import MailSender
import yaml

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.llm_agent = LLMAgent()
        self.mail_sender = MailSender()
        
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)

    def analyze_tasks(self):
        try:
            with open("data/memo.html", "r") as f:
                memo_content = f.read()
            
            tasks = self.llm_agent.analyze_memo(memo_content)
            self.llm_agent.save_todo(tasks)
            return tasks
        except Exception as e:
            print(f"Task analysis failed: {e}")
            return None

    def send_daily_email(self):
        try:
            tasks = self.analyze_tasks()
            if tasks:
                self.mail_sender.send_todo_list(tasks)
        except Exception as e:
            print(f"Email sending failed: {e}")

    def start(self):
        analyze_time = self.config["schedule"]["analyze_time"]
        email_time = self.config["schedule"]["email_time"]

        self.scheduler.add_job(
            self.analyze_tasks,
            CronTrigger.from_crontab(f"0 {analyze_time} * * *")
        )
        
        self.scheduler.add_job(
            self.send_daily_email,
            CronTrigger.from_crontab(f"0 {email_time} * * *")
        )
        
        self.scheduler.start()