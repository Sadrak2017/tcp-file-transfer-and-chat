class ProtocolHeader:

    def __init__(
        self,
        command: str,
        payload_size: int = 0,
        filename: str = "",
        filesize: int = 0,
        sha256: str = ""
    ):
        self.command = command
        self.payload_size = payload_size
        self.filename = filename
        self.filesize = filesize
        self.sha256 = sha256

    def to_dictionary(self):
        return {
            "command": self.command,
            "payload_size": self.payload_size,
            "filename": self.filename,
            "filesize": self.filesize,
            "sha256": self.sha256
        }