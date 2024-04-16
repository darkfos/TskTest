from abc import ABC, abstractmethod


class Crud(ABC):

    @abstractmethod
    async def get_one(self, *args, **kwargs):
        """
            Getting one record
        """
        pass

    @abstractmethod
    async def get_all(self, session):
        """
            Gettind all records
        """
        pass

    @abstractmethod
    async def add_one(self, *args):
        """
        Add a new object
        :param args:
        :return:
        """
        pass

    @abstractmethod
    async def del_one(self, *args, **kwargs):
        """
            Del one unique record
        """
        pass

    @abstractmethod
    async def update_one(self, *args, **kwargs):
        """
            Update one unique record
        """
        pass