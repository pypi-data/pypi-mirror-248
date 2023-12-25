from videoscope.errors.timecode_errors import TimeCodeErrors as TCErrors
from videoscope.config.timecode import TimeCodeConfig as TCConfig


class Timecode:
    def __init__(
        self, fps: float, start_timecode: str = TCConfig.DEF_TC, duration: float = 0.0
    ):
        # check dei parametri
        if duration < 0:
            raise ValueError(TCErrors.INVALID_DURATION_ERR)
        self.__duration: float = duration
        if fps <= 0:
            raise ValueError(TCErrors.INVALID_FPS_ERR)
        self.__fps: float = fps

        self.__validate_timecode(start_timecode)

        self.__start_timecode: str = start_timecode

        self.__duration_frames: int = 0
        self.__start_frame: int = 0
        self.__end_timecode: str = TCConfig.DEF_TC
        self.__end_frame: int = 0
        self.__recalculate_properties()

    @property
    def fps(self) -> float:
        return self.__fps

    @fps.setter
    def fps(self, value: float):
        self.__fps = float(value)
        self.__recalculate_properties()

    @property
    def duration(self) -> float:
        return self.__duration

    @duration.setter
    def duration(self, value: float):
        self.__duration = value
        self.__recalculate_properties()

    @property
    def start_timecode(self) -> str:
        return self.__start_timecode

    @start_timecode.setter
    def start_timecode(self, value: str):
        self.__validate_timecode(value)
        self.__start_timecode = value
        self.__recalculate_properties()

    @property
    def start_frame(self) -> int:
        return self.__start_frame

    @property
    def duration_frames(self) -> int:
        return self.__duration_frames

    @property
    def end_frame(self) -> int:
        return self.__end_frame

    @property
    def end_timecode(self) -> str:
        return self.__end_timecode

    def __validate_timecode(
        self, timecode: str, err_msg: str = TCErrors.INVALID_TC_ERR
    ) -> None:
        """Validate timecode format and its components."""
        if not isinstance(timecode, str):
            raise TypeError(f"{err_msg} {timecode}")

        components = timecode.split(":")

        # Verify there are exactly 4 components.
        if len(components) != 4:
            raise ValueError(f"{err_msg} {timecode}")

        # Check if all components are numbers and are in the valid range.
        hours, minutes, seconds, frames = map(int, components)
        if not (
            0 <= hours < 24
            and 0 <= minutes < 60
            and 0 <= seconds < 60
            and 0 <= frames < self.__fps
        ):
            raise ValueError(f"{err_msg} {timecode}")

    def __recalculate_properties(self):
        self.__duration_frames: int = int(self.__duration * self.__fps)
        self.__start_frame: int = self.timecode_to_frames(self.__start_timecode)
        end_frame = self.duration_frames - 1 if self.duration_frames > 0 else 0

        self.__end_timecode: str = self.frames_to_timecode(
            end_frame, start_timecode=self.__start_timecode
        )
        self.__end_frame: int = self.timecode_to_frames(self.__end_timecode)

    def _timecode_to_seconds(self, timecode) -> float:
        self.__validate_timecode(timecode)

        hours, minutes, seconds, frames = map(int, timecode.split(":"))
        return hours * 3600 + minutes * 60 + seconds + frames / self.fps

    def frames_to_timecode(
        self, frames: int, start_timecode: str = TCConfig.DEF_TC
    ) -> str:
        # Check for valid input
        if not isinstance(frames, int) or frames < 0:
            raise ValueError(TCErrors.INVALID_FRAME_ERR)

        self.__validate_timecode(start_timecode)

        # Convert start timecode to frames
        total_frames = self.timecode_to_frames(start_timecode) + frames
        return self._frames_to_timecode_logic(total_frames)

    def _frames_to_timecode_logic(self, total_frames):
        """Logic to convert frames to timecode."""
        frames_per_hour = self.__fps * 3600
        frames_per_minute = self.__fps * 60

        hours, total_frames = divmod(total_frames, frames_per_hour)
        minutes, total_frames = divmod(total_frames, frames_per_minute)
        seconds, frames = divmod(total_frames, self.__fps)

        timecode = (
            f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}:{int(frames):02d}"
        )

        self.__validate_timecode(timecode, err_msg=TCErrors.INVALID_RESULTANT_TC_ERR)
        return timecode

    def timecode_to_frames(self, timecode=TCConfig.DEF_TC) -> int:
        self.__validate_timecode(timecode)

        timecode = self.start_timecode if timecode is None else timecode

        return int(self._timecode_to_seconds(timecode) * self.fps)

    def get_timecode_at_frame(self, frame: int) -> str:
        if frame is None:
            frame = 0
        if not isinstance(frame, int) or frame < 0:
            raise ValueError(TCErrors.INVALID_FRAME_ERR)
        return self.frames_to_timecode(frame, start_timecode=self.start_timecode)

    def timecode_to_100ns_intervals(self, timecode) -> int:
        hours, minutes, seconds, frames = map(int, timecode.split(":"))

        # Converti tutto in secondi
        total_seconds = hours * 3600 + minutes * 60 + seconds + frames / self.__fps

        # Converti in intervalli da 100ns
        intervals_100ns = int(total_seconds * 10_000_000)

        return intervals_100ns
