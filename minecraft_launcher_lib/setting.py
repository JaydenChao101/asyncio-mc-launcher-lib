import logging
import requests

class LoggingSetting:
    def __init__(self, level: int = logging.INFO, filename: str = None, enable_console: bool = False):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        formatter = logging.Formatter("%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

        # 防止重复添加 handler
        if not self.logger.handlers:
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

class RequestsSetting:
    def __init__(
        self,
        timeout: float | tuple[float, float] = (5.0, 30.0),
        proxies: dict[str, str] = None,
        verify: bool | str = True,
        cert: str | tuple[str, str] = None,
        headers: dict[str, str] = None,
    ):
        """
        timeout: 单位秒或(connect, read)元组
        proxies: {'http': '...', 'https': '...'}
        verify: 是否校验证书或CA文件路径
        cert: 客户端证书路径或(cert.pem, key.pem)元组
        headers: 默认请求头
        """
        self.timeout = timeout
        self.proxies = proxies or {}
        self.verify = verify
        self.cert = cert
        self.headers = headers or {}
        self.session = requests.Session()
        # 应用默认配置
        if self.proxies:
            self.session.proxies.update(self.proxies)
        if self.cert:
            self.session.cert = self.cert
        self.session.verify = self.verify
        if self.headers:
            self.session.headers.update(self.headers)

    def request(self, method: str, url: str, **kwargs):
        # 合并默认设置
        kwargs.setdefault("timeout", self.timeout)
        if "proxies" not in kwargs and self.proxies:
            kwargs["proxies"] = self.proxies
        if "verify" not in kwargs:
            kwargs["verify"] = self.verify
        if "cert" not in kwargs and self.cert:
            kwargs["cert"] = self.cert
        # 合并 headers
        if "headers" in kwargs:
            h = dict(self.session.headers)
            h.update(kwargs["headers"])
            kwargs["headers"] = h
        return self.session.request(method, url, **kwargs)

    def get(self, url: str, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.request("POST", url, **kwargs)
