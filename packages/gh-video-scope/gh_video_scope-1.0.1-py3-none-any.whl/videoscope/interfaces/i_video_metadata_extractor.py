from abc import ABC, abstractmethod


class IMetadataExtractor(ABC):
    @abstractmethod
    def extract_metadata(self, file):
        pass
