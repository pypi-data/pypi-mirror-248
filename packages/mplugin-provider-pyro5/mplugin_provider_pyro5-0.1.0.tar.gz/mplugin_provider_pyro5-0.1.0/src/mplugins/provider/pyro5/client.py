import myrrh
import typing

from myrrh.provider import IProvider
from myrrh.core.interfaces import ABCDelegation

import threading
import Pyro5.api
from myrrh.provider._iservices import IService, ServiceGroup

from .config_client import DEFAULT_SECRET


class Pyro5ProviderSettings(myrrh.warehouse.Settings):
    name: typing.Literal["pyro5"] = "pyro5"

    cwd: str | None = None
    uri: str = "localhost:9999"
    timeout: float = Pyro5.config.COMMTIMEOUT
    max_retries: int = Pyro5.config.MAX_RETRIES


class Pyro5Proxy(Pyro5.api.Proxy):
    def __init__(self, settings: Pyro5ProviderSettings):
        super().__init__(settings.uri)

        self._pyroMaxRetries = settings.max_retries
        self._pyroTimeout = settings.timeout
        self._pyroHandshake = DEFAULT_SECRET

    def _pyroValidateHandshake(self, response):
        if response != self._pyroHandshake:
            raise RuntimeError("Handshake: invalid server response")


class LocalProxy(threading.local):
    def __init__(self, settings):
        self.proxy = Pyro5Proxy(settings)

    def __getattr__(self, name):
        return getattr(self.proxy, name)


class ProviderClient(IProvider, ABCDelegation):
    __delegated__ = (IProvider,)
    __delegate_check_type__ = False

    def __init__(self, settings=None):
        if not settings:
            settings = Pyro5ProviderSettings()

        self.settings = settings
        self.__delegate__(IProvider, LocalProxy(settings))

    def services(self) -> list[type[IService]]:
        result = list()
        services = self._delegate_.services()

        for s in services:
            settings = Pyro5ProviderSettings(**self.settings.model_dump())
            settings.uri = s
            proxy = LocalProxy(settings)
            category_ = proxy.category()
            name_ = proxy.name()
            protocol_ = proxy.protocol()

            Interface = ServiceGroup[category_].__interfaces__[name_]

            class ServiceAdapter(Interface, ABCDelegation):
                __delegated__ = (Interface, IService)
                __delegate_check_type__ = False

                category = category_
                name = name_
                protocol = protocol_

                def __init__(self, s=settings, i=Interface):
                    self.__delegate__(i, LocalProxy(s))

            result.append(ServiceAdapter)

        return result
