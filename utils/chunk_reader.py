class ChunkReader:

    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def read_chunks(self, file_object):
        while True:
            chunk = file_object.read(self.chunk_size)
            if not chunk:
                break
            yield chunk
