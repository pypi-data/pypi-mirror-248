class FormatMetadata:
    def __init__(
        self,
        filename,
        nb_streams,
        nb_programs,
        format_name,
        format_long_name,
        start_time,
        duration,
        size,
        bit_rate,
        probe_score,
        tags,
    ):
        self.filename = filename
        self.nb_streams = nb_streams
        self.nb_programs = nb_programs
        self.format_name = format_name
        self.format_long_name = format_long_name
        self.start_time = start_time
        self.duration = duration
        self.size = size
        self.bit_rate = bit_rate
        self.probe_score = probe_score
        self.tags = tags