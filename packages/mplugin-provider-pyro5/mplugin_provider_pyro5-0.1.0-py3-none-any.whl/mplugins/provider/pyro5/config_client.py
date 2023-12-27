from myrrh.core.services import cfg_init
from .config import config


config.SSL = cfg_init("use_ssl", False, "mplugins.provider.pyro5")
config.SSL_CACERTS = cfg_init("ca_cert", "", "mplugins.provider.pyro5")
config.SSL_CLIENTCERT = cfg_init("client_cert", "", "mplugins.provider.pyro5")
config.SSL_CLIENTKEY = cfg_init("client_key", "", "mplugins.provider.pyro5")

DEFAULT_SECRET = cfg_init("default_secret", "It's not a real secret", "mplugins.provider.pyro5")
