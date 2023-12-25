from abc import ABC, abstractmethod


class IThumbnailGenerator(ABC):
    @abstractmethod
    def generate_thumbnail(self, frame, factor):
        pass
