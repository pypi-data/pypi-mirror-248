VideoInfo Class Documentation
=============================

Overview
--------

The ``VideoInfo`` class is a comprehensive utility designed for handling
and extracting detailed information and metadata from video files. It
integrates with various subsystems to provide a wide range of data,
including audio, video, format, and data stream metadata, as well as
video thumbnails and timecode information.

Features
--------

-  **Video Handling**: Open and close video files, extracting basic
   stream information.
-  **Metadata Extraction**: Extract detailed metadata for video, audio,
   and data streams.
-  **Thumbnail Generation**: Generate thumbnails for video files based
   on a specified size factor.
-  **Timecode Analysis**: Calculate and provide timecode information for
   the video.

Components
----------

The class is composed of several components that work together to
provide a comprehensive set of information about a video file: -
``IVideoHandler``: Interface for handling basic video operations. -
``IMetadataExtractor``: Interface for extracting metadata from different
types of streams. - ``IThumbnailGenerator``: Interface for generating
thumbnails from video frames.

Usage
-----

To use the ``VideoInfo`` class, initialize it with the required handlers
and extractors specific to your video file’s needs. Once instantiated,
you can access various properties and methods to retrieve video
information and metadata.

.. code:: python

   video_info = VideoInfo(
       video_handler,
       audio_metadata_extractor,
       video_metadata_extractor,
       format_metadata_extractor,
       data_metadata_extractor,
       thumbnail_generator
   )

   print(video_info.fps)  # Access frame rate
   print(video_info.width)  # Access video width
   print(video_info.height)  # Access video height

Conclusion
----------

The ``VideoInfo`` class is a robust and flexible solution for anyone
looking to extract detailed information and metadata from video files.
With its comprehensive set of features and easy-to-use interface, it’s
an invaluable tool for developers working in video processing, editing,
and analysis.

--------------

*Note: This documentation is based on the provided class definition and
should be updated as the class evolves.*
