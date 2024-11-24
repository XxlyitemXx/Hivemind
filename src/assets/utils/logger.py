import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_dir = "logs"
        self.log_file = os.path.join(self.log_dir, f"bot_{datetime.now().strftime('%Y-%m-%d')}.log")
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def info(self, message, module=None):
        msg = f"[{module}] {message}" if module else message
        self.logger.info(msg)
    
    def error(self, message, module=None):
        msg = f"[{module}] {message}" if module else message
        self.logger.error(msg)
    
    def warning(self, message, module=None):
        msg = f"[{module}] {message}" if module else message
        self.logger.warning(msg)
    
    def command(self, user_id, command_name, status="executed"):
        self.info(f"User {user_id} {status} command: {command_name}", "COMMAND")
    
    def auth(self, user_id, action, status="success"):
        self.info(f"User {user_id} {action} - {status}", "AUTH")
    
    def get_logs(self, lines=50):
        if not os.path.exists(self.log_file):
            return "No logs found."
        
        with open(self.log_file, 'r') as file:
            logs = file.readlines()
            return ''.join(logs[-lines:])