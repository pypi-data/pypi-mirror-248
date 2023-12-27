import inspect
import sys

import Pyro5.server
import Pyro5.client

from myrrh.core.interfaces import DelegateProperty, ABCDelegation
from myrrh.provider import IProvider, IService, ServiceGroup, service_fullname

from mplugins.provider.local import Provider

import Pyro5.serializers

from .config_server import SECRET, PORT, config


class MyrrhDaemonObject(Pyro5.server.DaemonObject):
    def get_metadata(self, objectId):
        obj = self.daemon.objectsById.get(objectId)
        if obj is not None:
            metadata = self.daemon.get_exposed_delegated(obj)
            if not metadata["methods"] and not metadata["attrs"]:
                Pyro5.server.warnings.warn("Class %r doesn't expose any methods or attributes. Did you forget setting @expose on them?" % type(obj))
            return metadata
        else:
            Pyro5.server.log.debug("unknown object requested: %s", objectId)
            raise Pyro5.server.errors.DaemonError("unknown object")


class MyrrhDaemon(Pyro5.server.Daemon):
    def __init__(
        self,
        host=None,
        port=0,
        unixsocket=None,
        nathost=None,
        natport=None,
        connected_socket=None,
    ):
        super().__init__(
            host,
            port,
            unixsocket,
            nathost,
            natport,
            interface=MyrrhDaemonObject,
            connected_socket=connected_socket,
        )
        self._exposed_member_cache = {}

    def validateHandshake(self, conn, data):
        if data == SECRET:
            return SECRET
        else:
            raise ValueError("handshake failure, connection refused")

    def get_exposed_delegated(self, obj, only_exposed: bool = True):
        if not inspect.isclass(obj):
            obj = obj.__class__

        cache_key = (obj, only_exposed)
        if cache_key in self._exposed_member_cache:
            return self._exposed_member_cache[cache_key]

        exposed = Pyro5.server._get_exposed_members(obj, only_exposed=only_exposed)

        methods = exposed.get("methods") or set()
        oneway = exposed.get("oneway") or set()
        attrs = exposed.get("attrs") or set()

        delegated = getattr(obj, "__delegated__", None) or dict()

        for cls in delegated:
            for attr in cls.__abstractmethods__:
                if attr.startswith("_"):
                    continue

                v = inspect.getattr_static(obj, attr)

                if isinstance(v, DelegateProperty):
                    v._pyroExposed = True
                    v = getattr(v.cls, attr)

                if inspect.ismethod(v) or inspect.isfunction(v) or inspect.ismethoddescriptor(v):
                    v._pyroExposed = True
                    methods.add(attr)
                else:
                    attrs.add(attr)

        result = {"methods": methods, "oneway": oneway, "attrs": attrs}

        self._exposed_member_cache[cache_key] = result

        return result

    def proxyFor(self, objectOrId, nat=True):
        uri = self.uriFor(objectOrId, nat)
        proxy = Pyro5.client.Proxy(uri)

        try:
            registered_object = self.objectsById[uri.object]
        except KeyError:
            raise Pyro5.server.errors.DaemonError("object isn't registered in this daemon")

        meta = self.get_exposed_delegated(registered_object)
        proxy._pyroGetMetadata(known_metadata=meta)
        return proxy

    def register_service(self, Service: IService):
        Interface = ServiceGroup[Service.category].__interfaces__[Service.name]
        path = service_fullname(Service)

        @Pyro5.server.expose
        class ServiceAdapter(Service, ABCDelegation):
            __delegated__ = (Interface,)

            def category(self) -> str:
                return Service.category

            def name(self) -> str:
                return Service.name

            def protocol(self):
                return str(Service.protocol)

        return self.register(ServiceAdapter, objectId=path)


exposed_services = list()
_services = list()


@Pyro5.server.expose
class ProviderService(IProvider, ABCDelegation):
    __delegated__ = (IProvider,)

    def __init__(self):
        self.__delegate__(IProvider, Pyro5.server.expose(Provider)())

    def services(self):
        if not _services:
            alls = self._delegate_.services()
            for s in alls:
                _services.append(str(self._pyroDaemon.register_service(s)))

        return _services


def check_config():
    if config.SSL and not config.SSL_SERVERCERT:
        print("SSL option requires server certificate", file=sys.stderr)
        exit(-1)

    if config.SSL and not config.SSL_SERVERKEY:
        print("SSL option requires server key", file=sys.stderr)
        exit(-1)


def serve(port=PORT):
    check_config()
    daemon = MyrrhDaemon(port=port)
    uri = daemon.register(ProviderService, objectId="provider")
    print(f"Server started, uri: {uri}")
    daemon.requestLoop()
