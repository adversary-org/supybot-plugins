# Stub so local is a module, used for third-party modules
import requests

from .cargs import permanent
ca = permanent.client_args
domain = "https://api.btcmarkets.net"
uri = "/market/BTC/AUD/tick"
url = "{0}{1}".format(domain, uri)
try:
    r = requests.get(url, verify=True, headers=ca["headers"],
                     proxies=ca["proxies"])
    # r = requests.get(url, verify=True)
except:
    r = None
    pass
