import os
import numpy as np
from videoscope.errors.file_handle_errors import FileHandlerErrors
from videoscope.interfaces.i_video_handler import IVideoHandler


import ffmpeg


class FFmpegVideoHandler(IVideoHandler):
    def __init__(self, path):
        self.path = path
        self.file = None

    def open_video(self):
        if os.path.isfile(self.path):
            self.file = ffmpeg.input(self.path)
            return self.file
        else:
            raise ValueError(FileHandlerErrors.FILE_NOT_EXIST)

    def get_probe(self):
        return ffmpeg.probe(self.path)

    def get_first_frame(self, width, height, pix_fmt="bgr24"):
        out, _ = self.file.output(
            "pipe:", format="rawvideo", pix_fmt=pix_fmt, vframes=1
        ).run(capture_stdout=True, capture_stderr=True)
        frame = np.frombuffer(out, np.uint8).reshape([height, width, 3])
        return frame

    def close_video(self):
        self.file = None
