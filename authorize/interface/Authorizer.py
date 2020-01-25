import abc


class Authorizer(abc.ABC):

    @abc.abstractmethod
    def token(self):
        pass

    @abc.abstractmethod
    def authorize(self):
        pass

    