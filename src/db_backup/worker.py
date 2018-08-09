import importlib


class Worker:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        clazz = getattr(importlib.import_module('.db', package='db.backup'), self.kwargs['db'])
        self.db = clazz(**self.kwargs)
        self.name = self.db.name
        self.storages = list()
        for storage in self.kwargs['storages']:
            clazz = getattr(importlib.import_module('.storage', package='db.backup'), storage['provider'])
            self.storages.append(clazz(**storage))

    def work(self):
        results = self.db.backup()
        for storage in self.storages:
            storage.store(**results)
