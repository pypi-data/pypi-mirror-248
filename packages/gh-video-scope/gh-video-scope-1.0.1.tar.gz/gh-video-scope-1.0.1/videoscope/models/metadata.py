class Metadata:
    def __init__(self, metadata_dict):
        for key, value in metadata_dict.items():
            setattr(self, key, value)

    def __str__(self):
        return str(self.__dict__)