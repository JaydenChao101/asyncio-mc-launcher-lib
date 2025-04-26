# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause

from minecraft_launcher_lib.setting import LoggingSetting
import logging

# 初始化全局 logger，可根据需要自定义名称、级别和格式
logger = LoggingSetting(level=logging.INFO, enable_console=False).logger

from . import (
    command,
    install,
    microsoft_account,
    utils,
    java_utils,
    forge,
    fabric,
    quilt,
    news,
    runtime,
    vanilla_launcher,
    mrpack,
    exceptions,
    _types,
    microsoft_types,
)

__all__ = [
    "command",
    "install",
    "microsoft_account",
    "utils",
    "news",
    "java_utils",
    "forge",
    "fabric",
    "quilt",
    "runtime",
    "vanilla_launcher",
    "mrpack",
    "exceptions",
    "_types.py",
    "microsoft_types",
    "logger",
]
