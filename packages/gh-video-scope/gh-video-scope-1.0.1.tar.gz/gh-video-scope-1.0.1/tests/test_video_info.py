import unittest
from videoscope import (
    VideoInfo,
    FFmpegVideoHandler,
    VideoMetadataExtractor,
    OpenCVThumbnailGenerator,
)


class TestVideoInfo(unittest.TestCase):
    def setUp(self):
        # Inizializza qui le risorse necessarie per i test
        self.video_handler = FFmpegVideoHandler()
        self.metadata_extractor = VideoMetadataExtractor()
        self.thumbnail_generator = OpenCVThumbnailGenerator()
        self.video_path = "path/to/test/video.mp4"  # Sostituire con il percorso di un video di test reale
        self.video_info = VideoInfo(
            self.video_handler,
            self.metadata_extractor,
            self.thumbnail_generator,
            self.video_path,
        )

    def test_metadata_extraction(self):
        # Test per l'estrazione dei metadati
        metadata = self.video_info.metadata
        self.assertIsNotNone(metadata, "I metadati non dovrebbero essere None")

    def test_thumbnail_generation(self):
        # Test per la generazione della miniatura
        thumbnail = self.video_info.thumbnail
        self.assertIsNotNone(thumbnail, "La miniatura non dovrebbe essere None")

    def test_invalid_video_path(self):
        # Test per verificare il comportamento con un percorso video non valido
        with self.assertRaises(ValueError):
            invalid_video_info = VideoInfo(
                self.video_handler,
                self.metadata_extractor,
                self.thumbnail_generator,
                "path/to/nonexistent/video.mp4",
            )


# Questo permette di eseguire i test se questo script viene eseguito direttamente
if __name__ == "__main__":
    unittest.main()
