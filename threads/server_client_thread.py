import threading
from protocol.protocol_command import ProtocolCommand
from protocol.protocol_header import ProtocolHeader
from services.directory_security_service import DirectorySecurityService
from services.file_integrity_service import FileIntegrityService
from services.file_transfer_service import FileTransferService


class ServerClientThread(threading.Thread):

    def __init__(self, connection_handler, chat_broadcast_service):
        super().__init__()
        self.connection_handler = connection_handler
        self.chat_broadcast_service = chat_broadcast_service
        self.directory_security_service = DirectorySecurityService()
        self.file_integrity_service = FileIntegrityService()
        self.file_transfer_service = FileTransferService()

    def run(self):
        self.chat_broadcast_service.register_connected_client(self.connection_handler)
        client_address = self.connection_handler.get_socket_connection().getpeername()
        print(f"[SERVER] Cliente conectado {client_address[0]}:{client_address[1]}")

        try:
            while True:
                (protocol_header, payload) = self.connection_handler.receive_message()
                print(
                    f"[SERVER] Command={protocol_header.command} "
                    f"PayloadSize={protocol_header.payload_size}"
                )
                command = protocol_header.command
                if command == ProtocolCommand.EXIT:
                    print(f"[SERVER] Cliente solicitou desconexão {client_address[0]}:{client_address[1]}")
                    break

                if command == ProtocolCommand.CHAT:
                    original_message = payload.decode("utf-8")
                    print(
                        f"[CHAT] {client_address[0]}:{client_address[1]} -> "
                        f"{original_message}"
                    )
                    broadcast_message = (
                        f"{client_address[0]}:{client_address[1]} - "
                        f"{original_message}"
                    )
                    broadcast_payload = broadcast_message.encode("utf-8")
                    protocol_header.payload_size = len(broadcast_payload)
                    self.chat_broadcast_service.broadcast_message(
                        protocol_header,
                        broadcast_payload
                    )
                if command == ProtocolCommand.DOWNLOAD:
                    filename = payload.decode("utf-8")
                    print(
                        f"[DOWNLOAD] Solicitação recebida "
                        f"cliente={client_address[0]}:{client_address[1]} "
                        f"arquivo='{filename}'"
                    )

                    self.process_download_request(filename)

        except Exception as exception:
            print(f"[SERVER][ERROR] {exception}")
        finally:
            self.chat_broadcast_service.unregister_connected_client(self.connection_handler)
            self.connection_handler.close_connection()
            print(
                f"[SERVER] Cliente desconectado "
                f"{client_address[0]}:{client_address[1]}"
            )

    def process_download_request(self, filename):
        try:
            print(f"[DOWNLOAD] Validando arquivo '{filename}'")
            file_path = self.directory_security_service.validate_file_exists(filename)
            print(f"[DOWNLOAD] Arquivo encontrado: {file_path}")
            sha256 = self.file_integrity_service.calculate_file_sha256(file_path)
            print(f"[DOWNLOAD] SHA256: {sha256}")
            metadata = self.file_transfer_service.create_file_metadata(
                file_path,
                sha256
            )
            print(
                f"[DOWNLOAD] Metadata criada "
                f"filename={metadata.filename} "
                f"filesize={metadata.filesize}"
            )
            self.file_transfer_service.send_file_metadata(
                self.connection_handler,
                metadata
            )
            print("[DOWNLOAD] Metadata enviada")
            self.file_transfer_service.send_file_chunks(
                self.connection_handler,
                file_path
            )
            print(f"[DOWNLOAD] Transferência concluída '{filename}'")
        except Exception as exception:
            print(f"[DOWNLOAD][ERROR] {exception}")
            self.connection_handler.send_message(
                ProtocolHeader(
                    command=ProtocolCommand.ERROR,
                    payload_size=len(str(exception).encode("utf-8"))
                ),
                str(exception).encode("utf-8")
            )
