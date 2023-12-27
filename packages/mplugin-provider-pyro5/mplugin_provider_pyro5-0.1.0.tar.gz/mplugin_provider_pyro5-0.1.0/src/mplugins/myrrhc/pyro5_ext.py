import Pyro5
import Pyro5.nsc

from mplugins.myrrhc.provider_ext import provider, cmd, types


@provider.group()
def pyro5():
    ...


@pyro5.group()
def config():
    ...


@config.command(help=Pyro5.configure.global_config.dump.__doc__)
def dump():
    cmd.info(Pyro5.configure.global_config.dump())


@config.command(help=Pyro5.configure.global_config.reset.__doc__)
def reset():
    Pyro5.configure.global_config.reset()
    Pyro5.configure.global_config.SERPENT_BYTES_REPR = True
    dump()


@config.group(help="set configuration item")
def set():
    ...


@config.group(help="get configuration item value")
def get():
    ...


for item, type_, nargs in (
    ("HOST", types.STRING, 1),
    ("NS_HOST", types.STRING, 1),
    ("NS_PORT", types.INT, 1),
    ("NS_BCPORT", types.INT, 1),
    ("NS_BCHOST", types.INT, 1),
    ("NS_AUTOCLEAN", types.FLOAT, 1),
    ("NS_LOOKUP_DELAY", types.FLOAT, 1),
    ("COMPRESSION", types.BOOL, 1),
    ("BROADCAST_ADDRS", types.STRING, -1),
    ("PREFER_IP_VERSION", types.INT, 1),
    ("LOGWIRE", types.STRING, 1),
    ("LOGFILE", types.STRING, 1),
    ("LOGLEVEL", types.INT, 1),
    ("MAX_RETRIES", types.INT, 1),
    ("COMMTIMEOUT", types.FLOAT, 1),
    ("DETAILED_TRACEBACK", types.BOOL, 1),
    ("SSL", types.BOOL, 1),
    ("SSL_CLIENTCERT", types.STRING, 1),
    ("SSL_CLIENTKEY", types.STRING, 1),
    ("SSL_CLIENTKEYPASSWD", types.STRING, 1),
    ("SSL_CACERTS", types.STRING, 1),
):

    @get.command(name=item.lower())
    def _get(item=item):
        cmd.info(f"{item}={getattr(Pyro5.configure.global_config, item)}")

    @set.command(name=item.lower())
    @cmd.argument("value", metavar=item, type=type_, nargs=nargs)
    def _set(value, item=item):
        setattr(Pyro5.configure.global_config, item, value)
        cmd.info(f"{item}={getattr(Pyro5.configure.global_config, item)}")


@pyro5.command(help=Pyro5.nsc.__doc__)
@cmd.option("-n", "--host", help="hostname of the NS", default="")
@cmd.option("-p", "--port", type=int, help="port of the NS (or bc-port if host isn't specified)")
@cmd.option("-u", "--unixsocket", help="Unix domain socket name of the NS")
@cmd.option("-v", "--verbose", is_flag=True, default=False, help="verbose output")
@cmd.argument(
    "command",
    type=types.Choice(
        (
            "list",
            "lookup",
            "register",
            "remove",
            "removematching",
            "listmatching",
            "yplookup_all",
            "yplookup_any",
            "setmeta",
            "ping",
        )
    ),
)
def nsc(host, port, unixsocket, verbose, command):
    args = list()
    if host:
        args.extend(["-h", host])
    if port:
        args.extend(["-p", port])
    if unixsocket:
        args.extend(["-u", unixsocket])
    if verbose:
        args.extend(["-v"])

    args.extend([command])

    Pyro5.nsc.main(args)


@pyro5.command()
def pyinstall():
    try:
        import PyInstaller.__main__
    except ImportError:
        cmd.error("pyinstall command requires PyInstaller")
        return

    import mplugins.scripts.myrrh_pyro5s

    try:
        PyInstaller.__main__.run(["-F", mplugins.scripts.myrrh_pyro5s.__file__])
    except SystemExit as e:
        cmd.error(str(e))
