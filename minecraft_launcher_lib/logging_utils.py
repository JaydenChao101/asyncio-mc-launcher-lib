import logging
from minecraft_launcher_lib.setting import setup_logger

# 初始化全局 logger
logger = setup_logger(
    name="minecraft_launcher_lib",
    level=logging.INFO,
    filename="minecraft_launcher_lib.log",
    enable_console=False,
)
