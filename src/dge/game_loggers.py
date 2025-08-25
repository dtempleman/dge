from typing import List
from datetime import datetime


class GameLogger:
    def __init__(self) -> None:
        self.log_stack: List[str] = []

    def log(self, log_message: str, log_level: str = "DEBUG"):
        timestamp_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_stack.append(f"[{timestamp_string}][{log_level}]: {log_message}")
