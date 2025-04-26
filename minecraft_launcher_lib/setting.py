import logging


class LoggingSetting:
    def __init__(
        self,
        level: int = logging.INFO,
        filename: str = None,
        enable_console: bool = False,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
        )

        if enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if filename:
            file_handler = logging.FileHandler(filename)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
