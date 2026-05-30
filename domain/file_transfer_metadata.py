class FileTransferMetadata:

    def __init__(self, filename: str, filesize: int, sha256: str):
        self.filename = filename
        self.filesize = filesize
        self.sha256 = sha256

    def get_filename(self):
        return self.filename

    def get_filesize(self):
        return self.filesize

    def get_sha256(self):
        return self.sha256
