import logging
from launcher_core.setting import setup_logger

# 初始化全局 logger
logger = setup_logger(
    name="launcher_core",
    level=logging.INFO,
    enable_console=False,
)
