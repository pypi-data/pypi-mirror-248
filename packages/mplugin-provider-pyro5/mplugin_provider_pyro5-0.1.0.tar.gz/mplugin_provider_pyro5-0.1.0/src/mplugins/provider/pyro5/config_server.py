import optparse

from .config import config

option_list = [
    optparse.make_option("--hostname", action="store", default="127.0.0.1", dest="hostname"),
    optparse.make_option("--secret", action="store", default="It's not a real secret", dest="secret"),
    optparse.make_option("--port", action="store", dest="port"),
    optparse.make_option("--cert", action="store", dest="certificate"),
    optparse.make_option("--key", action="store", dest="key"),
    optparse.make_option("--ssl", action="store_true", dest="ssl"),
    optparse.make_option("--logwire", action="store_true", dest="logwire"),
    optparse.make_option("--logfile", action="store", dest="logfile"),
    optparse.make_option("--loglevel", action="store", type=int, dest="loglevel"),
    optparse.make_option("--print-config", action="store_true", dest="print_config"),
]

parser = optparse.OptionParser(option_list=option_list)
options, _ = parser.parse_args()


config.HOST = options.hostname
config.SSL = options.ssl
config.SSL_SERVERCERT = options.certificate
config.SSL_SERVERKEY = options.key
config.LOGWIRE = options.logwire
config.LOGFILE = options.logfile
config.LOGLEVEL = options.loglevel

SECRET = options.secret
PORT = options.port and int(options.port) or 9999

if options.print_config:
    print(config.dump())
    exit(0)
