import logging
import sys
from pythonjsonlogger.json import JsonFormatter  # updated for v3.x


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # safely copy log level & function name
        log_record["log_level"] = log_record.get("levelname", record.levelname)
        log_record["function_name"] = log_record.get("funcName", record.funcName)

        # safely remove keys
        for key in ("asctime", "name", "levelname", "funcName"):
            log_record.pop(key, None)


class Logger:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.handlers.clear()  # cleaner way to remove old handlers

        handler = logging.StreamHandler(sys.stdout)
        formatter = CustomJsonFormatter(
            "%(asctime)s - %(name)s - %(funcName)s - %(message)s"
        )
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)


logger = Logger().logger
