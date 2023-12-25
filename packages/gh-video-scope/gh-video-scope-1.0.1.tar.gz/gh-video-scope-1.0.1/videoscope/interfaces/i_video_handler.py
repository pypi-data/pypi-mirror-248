from abc import ABC, abstractmethod


class IVideoHandler(ABC):
    @abstractmethod
    def open_video(self):
        pass

    @abstractmethod
    def close_video(self):
        pass