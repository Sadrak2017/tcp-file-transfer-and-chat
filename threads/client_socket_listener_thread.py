import threading
from protocol.protocol_command import ProtocolCommand
from configuration.storage_configuration import StorageConfiguration
from services.file_integrity_service import FileIntegrityService
from services.file_transfer_service import FileTransferService


class ClientSocketListenerThread(threading.Thread):

    def __init__(self, connection_handler):
        super().__init__(daemon=True)
        self.connection_handler = connection_handler
        self.file_transfer_service = FileTransferService()
        self.file_integrity_service = FileIntegrityService()

    def run(self):
        while True:
            try:
                (protocol_header, payload) = self.connection_handler.receive_message()
                command = protocol_header.command
                if command == ProtocolCommand.CHAT:
                    print(f"\n{payload.decode('utf-8')}")
                elif command == ProtocolCommand.ERROR:
                    print()
                    print("=" * 60)
                    print(f"ERROR: {payload.decode('utf-8')}")
                    print("=" * 60)
                    print()
                elif command == ProtocolCommand.FILE and protocol_header.filesize > 0:
                    self.receive_file(protocol_header)
            except Exception:
                break

    def receive_file(self, protocol_header):
        destination_path = StorageConfiguration.DOWNLOAD_DIRECTORY / protocol_header.filename
        self.file_transfer_service.save_received_file(destination_path, protocol_header.filesize, self.connection_handler)
        if self.file_integrity_service.validate_file_integrity(destination_path, protocol_header.sha256):
            print(f"\nArquivo recebido: {protocol_header.filename}")
            print(f"SHA256 validado: {protocol_header.sha256}")
        else:
            print("\nFalha de integridade")