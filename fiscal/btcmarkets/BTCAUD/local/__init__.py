# Stub so local is a module, used for third-party modules
from . import cleanup
from .cargs import permanent

ca = permanent.client_args
domain = "https://api.btcmarkets.net"
uri = "/market/BTC/AUD/tick"
url = "{0}{1}".format(domain, uri)

