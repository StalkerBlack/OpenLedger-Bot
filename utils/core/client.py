import random


class Client:
    def __init__(
            self, name: str, proxy: str, token: str = None,
        ):
        self.name = name
        self.proxy_init = proxy
        self.request_kwargs = {"proxy": f'{proxy}', "verify_ssl": False} if proxy else {"verify_ssl": False}
        self.token = token
    
    @staticmethod
    def get_user_agent() -> str:
        chrome_version = f"{random.randint(90, 121)}.0.{random.randint(1000, 9999)}.{random.randint(0, 99)}"
        safari_version = f"{random.uniform(600, 610):.2f}"
        return (f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{safari_version} '
                f'(KHTML, like Gecko) Chrome/{chrome_version} Safari/{safari_version}')