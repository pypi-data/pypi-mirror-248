from videoscope.interfaces.i_thumbnail_generator import IThumbnailGenerator


import cv2


class OpenCVThumbnailGenerator(IThumbnailGenerator):
    def generate_thumbnail(self, frame, factor):
        size = frame.shape
        return cv2.resize(frame, (int(size[1] * factor), int(size[0] * factor)))
