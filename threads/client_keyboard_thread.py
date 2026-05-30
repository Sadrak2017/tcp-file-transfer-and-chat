import threading
from protocol.protocol_command import ProtocolCommand
from protocol.protocol_header import ProtocolHeader


class ClientKeyboardThread(threading.Thread):

    def __init__(self, connection_handler):
        super().__init__()
        self.connection_handler = connection_handler

    def show_menu(self):
        print()
        print("================================")
        print("1 - Chat")
        print("2 - Download")
        print("3 - Sair")
        print("================================")

    def run(self):
        self.show_menu()
        while True:
            option = input("> ")
            if option == "1":
                self.send_chat_message()
            elif option == "2":
                self.request_download()
            elif option == "3":
                self.exit_application()
                break

    def send_chat_message(self):
        message = input("Diga: ")
        payload = message.encode("utf-8")

        self.connection_handler.send_message(
            ProtocolHeader(
                command=ProtocolCommand.CHAT,
                payload_size=len(payload)
            ),
            payload
        )

    def request_download(self):
        filename = input("Arquivo: ")
        payload = filename.encode("utf-8")
        self.connection_handler.send_message(
            ProtocolHeader(command=ProtocolCommand.DOWNLOAD, payload_size=len(payload)),
            payload
        )

    def exit_application(self):
        self.connection_handler.send_message(ProtocolHeader(command=ProtocolCommand.EXIT))
        self.connection_handler.close_connection()