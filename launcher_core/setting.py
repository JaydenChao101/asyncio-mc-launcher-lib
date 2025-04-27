import logging


def setup_logger(
    name: str = None,
    level: int = logging.INFO,
    filename: str = None,
    enable_console: bool = False,
) -> logging.Logger:
    """
    設定並返回一個 logger。

    :param name: Logger 的名稱，默認為 None（根 logger）。
    :param level: 日誌級別，默認為 logging.INFO。
    :param filename: 如果提供，日誌將寫入該文件。
    :param enable_console: 如果為 True，日誌將輸出到控制台。
    :return: 配置好的 logger。
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 添加控制台處理器
    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # 添加文件處理器
    if filename:
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
