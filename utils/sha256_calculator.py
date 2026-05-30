import hashlib


class Sha256Calculator:

    def __init__(self, chunk_size: int = 8192):
        self.chunk_size = chunk_size

    def calculate_file_sha256(self, file_path) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as file_object:
            while True:
                chunk = file_object.read(self.chunk_size)
                if not chunk:
                    break
                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()
