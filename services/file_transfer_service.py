from pathlib import Path
from configuration.storage_configuration import StorageConfiguration
from domain.file_transfer_metadata import FileTransferMetadata
from protocol.protocol_command import ProtocolCommand
from protocol.protocol_header import ProtocolHeader
from utils.chunk_reader import ChunkReader


class FileTransferService:

    def __init__(self):
        self.chunk_reader = ChunkReader(StorageConfiguration.FILE_CHUNK_SIZE)

    @staticmethod
    def create_file_metadata(file_path: Path, sha256: str) -> FileTransferMetadata:
        return (
            FileTransferMetadata(
                filename=file_path.name,
                filesize=file_path.stat().st_size,
                sha256=sha256
            )
        )

    @staticmethod
    def send_file_metadata(connection_handler, metadata: FileTransferMetadata):
        protocol_header = (
            ProtocolHeader(
                command=ProtocolCommand.FILE,
                filename=metadata.filename,
                filesize=metadata.filesize,
                sha256=metadata.sha256
            )
        )
        connection_handler.send_message(protocol_header)

    def send_file_chunks(self, connection_handler, file_path: Path):
        client_address = connection_handler.get_socket_connection().getpeername()

        total_size = file_path.stat().st_size
        bytes_sent = 0
        chunk_count = 0
        last_percent = -1

        print(
            f"[DOWNLOAD] Iniciando envio "
            f"cliente={client_address[0]}:{client_address[1]} "
            f"arquivo='{file_path.name}' "
            f"tamanho={total_size} bytes"
        )

        with open(file_path, "rb") as file_object:
            for chunk in self.chunk_reader.read_chunks(file_object):
                protocol_header = (
                    ProtocolHeader(
                        command=ProtocolCommand.FILE,
                        payload_size=len(chunk)
                    )
                )

                connection_handler.send_message(protocol_header, chunk)

                chunk_count += 1
                bytes_sent += len(chunk)

                percent = int((bytes_sent / total_size) * 100)

                if percent >= last_percent + 10:
                    print(
                        f"[DOWNLOAD] "
                        f"cliente={client_address[0]}:{client_address[1]} "
                        f"progresso={percent}% "
                        f"({bytes_sent}/{total_size} bytes)"
                    )
                    last_percent = percent

        print(
            f"[DOWNLOAD] Concluído "
            f"cliente={client_address[0]}:{client_address[1]} "
            f"arquivo='{file_path.name}' "
            f"chunks={chunk_count} "
            f"bytes={bytes_sent}"
        )
    @staticmethod
    def save_received_file(destination_file_path: Path, total_file_size: int, connection_handler):
        destination_file_path.parent.mkdir(parents=True, exist_ok=True)
        received_bytes = 0
        with open(destination_file_path, "wb") as file_object:
            while received_bytes < total_file_size:
                (protocol_header, payload) = connection_handler.receive_message()
                file_object.write(payload)
                received_bytes += len(payload)