__all__ = []

from abc import ABCMeta, abstractmethod

from attr import attrib, attrs


@attrs(kw_only=True)
class CommonClient(metaclass=ABCMeta):
    _client = attrib(init=False, default=None)
    _config = attrib()
    _logger = attrib()

    @abstractmethod
    def _connect(self):
        pass

    @property
    def client(self):
        """returns client"""
        if self._client is None:
            self._client = self._connect()
        return self._client

    @property
    def config(self):
        """returns client specific subset configuration"""
        return self._config

    @property
    def logger(self):
        """returns parent logger"""
        return self._logger
