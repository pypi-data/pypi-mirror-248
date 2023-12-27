
import pyhttpx
from loguru import logger

from .base import BaseCracker

import warnings
warnings.filterwarnings('ignore')


class CloudFlareCracker(BaseCracker):
    
    cracker_name = "cloudflare"
    cracker_version = "universal"    

    """
    cloudflare cracker
    :param href: 触发 cloudfalre 验证的首页地址
    :param user_agent: 请求流程使用 ua, 必须使用 Chrome User-Agent, 否则可能破解失败
    :param headers: 触发验证必须的 headers, 默认 {} 
    :param cookies: 触发验证必须的 cookies, 默认 {} 
    调用示例:
    cracker = CloudFlareCracker(
        href=href,
        user_token="xxx",
    )
    ret = cracker.crack()
    """
    
    # 必传参数
    must_check_params = ["href"]
    # 默认可选参数
    option_params = {
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0",
        "headers": {},
        "cookies": {},
        "proxy": None
    }
