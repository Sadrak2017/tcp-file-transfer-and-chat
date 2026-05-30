from pathlib import Path


class StorageConfiguration:

    ROOT_DIRECTORY = Path("storage/dataset")
    DOWNLOAD_DIRECTORY = Path("storage/downloads")
    FILE_CHUNK_SIZE = 8192
