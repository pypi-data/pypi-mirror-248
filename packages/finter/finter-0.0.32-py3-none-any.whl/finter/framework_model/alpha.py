from abc import ABCMeta, abstractmethod
from finter.framework_model import ContentModelLoader


class BaseAlpha(metaclass=ABCMeta):
    __CM_LOADER = ContentModelLoader()

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance.cm_set = set()
        return instance

    @abstractmethod
    def get(self, start, end):
        pass

    def get_cm(self, key):
        if key.startswith("content."):
            self.cm_set.add(key)
        else:
            self.cm_set.add('content.' + key)
        return BaseAlpha.__CM_LOADER.load(key)

    def depends(self):
        return self.cm_set
