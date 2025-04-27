import logging
from launcher_core.setting import setup_logger

# 初始化全局 logger
logger = setup_logger(
    name="minecraft_launcher_lib",
    level=logging.INFO,
    filename="launcher_corelog",
    enable_console=False,
)
