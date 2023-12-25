from fractions import Fraction
from videoscope.models.timecode import Timecode
from videoscope.interfaces.i_thumbnail_generator import IThumbnailGenerator
from videoscope.interfaces.i_video_metadata_extractor import IMetadataExtractor
from videoscope.interfaces.i_video_handler import IVideoHandler
from videoscope.errors.video_info_errors import VideoInfoErrors


class VideoInfo:
    """
    A class representing the information and metadata of a video file.

    Attributes:
        video_handler (IVideoHandler): An instance responsible for handling video operations.
        audio_metadata_extractor (IMetadataExtractor): An instance for extracting audio metadata.
        video_metadata_extractor (IMetadataExtractor): An instance for extracting video metadata.
        format_metadata_extractor (IMetadataExtractor): An instance for extracting format metadata.
        data_metadata_extractor (IMetadataExtractor): An instance for extracting data stream metadata.
        thumbnail_generator (IThumbnailGenerator): An instance responsible for generating thumbnails.
        thumbnail_factor (float): A factor determining the size of the generated thumbnail relative to the video.
        video_path (str): The path to the video file.
        file: A file object representing the opened video file.
        audios_metadata (list): A list of metadata objects for each audio stream in the video.
        video_metadata: The metadata for the video stream.
        data_metadata (list): A list of metadata objects for each data stream in the video.
        format_metadata: The metadata for the video file format.
        first_frame: The first frame of the video.
        thumbnail: The generated thumbnail image for the video.
        timecode (Timecode): An object representing the timecode information of the video.

    Methods:
        __init__: Constructs all the necessary attributes for the VideoInfo object.
        __initialize_file: Initializes the video file and extracts basic stream information.
        __initialize_video_info: Extracts all metadata and initializes additional information like the first frame and thumbnail.
        fps: Returns the frame rate of the video.
        width: Returns the width of the video.
        height: Returns the height of the video.
        __str__: Returns a string representation of the VideoInfo object, typically the video path.
    """

    def __init__(
        self,
        video_handler: IVideoHandler,
        audio_metadata_extractor: IMetadataExtractor,
        video_metadata_extractor: IMetadataExtractor,
        format_metadata_extractor: IMetadataExtractor,
        data_metadata_extractor: IMetadataExtractor,
        thumbnail_generator: IThumbnailGenerator,
        thumbnail_factor=0.25,
    ):
        """
        Constructs all the necessary attributes for the VideoInfo object from the provided parameters.

        Parameters:
            video_handler (IVideoHandler): Handler for video operations.
            audio_metadata_extractor (IMetadataExtractor): Extractor for audio metadata.
            ... (continued for each parameter) ...
            thumbnail_factor (float, optional): Factor for thumbnail size. Defaults to 0.25.
        """
        self.video_handler = video_handler
        self.audio_metadata_extractor: IMetadataExtractor = audio_metadata_extractor
        self.video_metadata_extractor: IMetadataExtractor = video_metadata_extractor
        self.format_metadata_extractor: IMetadataExtractor = format_metadata_extractor
        self.data_metadata_extractor: IMetadataExtractor = data_metadata_extractor
        self.thumbnail_generator: IThumbnailGenerator = thumbnail_generator
        self.video_path: str = None
        self.thumbnail_factor: float = thumbnail_factor
        self.file = None
        self.audios_metadata = []
        self.video_metadata = None
        self.data_metadata = []
        self.format_metadata = None
        self.first_frame = None
        self.thumbnail = None
        self.timecode: Timecode = None
        self.__initialize_file()
        self.__initialize_video_info()

    def __initialize_file(self):
        """
        Initializes the video file, opening it, probing for data, and extracting basic stream information.
        Sets up video, audio, and data streams and checks for the presence of a video stream.
        """
        self.file = self.video_handler.open_video()
        self._probe_data = self.video_handler.get_probe()
        self.video_path = self.video_handler.path
        self.__video_stream = next(
            (
                stream
                for stream in self._probe_data["streams"]
                if stream["codec_type"] == "video"
            ),
            None,
        )
        if self.__video_stream is None:
            raise ValueError(VideoInfoErrors.NO_VIDEO_STREAM_FOUND)

        self.__audio_streams = [
            stream
            for stream in self._probe_data["streams"]
            if stream.get("codec_type") == "audio"
        ]

        self.__data_streams = [
            stream
            for stream in self._probe_data["streams"]
            if stream.get("codec_type") == "data"
        ]

    def __initialize_video_info(self):
        """
        Extracts detailed metadata for video, audio, and data streams. Generates the first frame and thumbnail of the video.
        Initializes the timecode if applicable.
        """
        try:
            self.video_metadata = self.video_metadata_extractor.extract_metadata(
                self.__video_stream
            )

            self.audios_metadata = [
                self.audio_metadata_extractor.extract_metadata(stream)
                for stream in self.__audio_streams
            ]

            self.format_metadata = self.format_metadata_extractor.extract_metadata(
                self._probe_data["format"]
            )

            self.data_metadata = [
                self.data_metadata_extractor.extract_metadata(stream)
                for stream in self.__data_streams
            ]

            self.first_frame = self.video_handler.get_first_frame(
                self.video_metadata.width, self.video_metadata.height
            )

            self.thumbnail = self.thumbnail_generator.generate_thumbnail(
                self.first_frame,
                self.thumbnail_factor,
            )

            frame_rate = None
            if self.video_metadata.r_frame_rate:
                frame_rate = float(Fraction(self.video_metadata.r_frame_rate))
            elif self.video_metadata.frame_rate:
                float(Fraction(self.video_metadata.frame_rate))

            if frame_rate and hasattr(self.format_metadata, "tags"):
                self.timecode = Timecode(
                    frame_rate,
                    self.format_metadata.tags.get("timecode", "00:00:00:00"),
                    float(self.format_metadata.duration),
                )

        finally:
            self.video_handler.close_video()

    @property
    def fps(self):
        """
        Returns the frame rate of the video.

        Returns:
            str: The frame rate of the video.
        """
        return self.video_metadata.r_frame_rate

    @property
    def width(self):
        """
        Returns the width of the video.

        Returns:
            int: The width of the video in pixels.
        """
        return self.video_metadata.width

    @property
    def height(self):
        """
        Returns the height of the video.

        Returns:
            int: The height of the video in pixels.
        """
        return self.video_metadata.height

    def __str__(self) -> str:
        """
        Returns a string representation of the VideoInfo object.

        Returns:
            str: The video path.
        """
        return f"{self.video_path}"
