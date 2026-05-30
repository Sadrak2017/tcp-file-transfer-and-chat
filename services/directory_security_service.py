from pathlib import Path
from configuration.storage_configuration import StorageConfiguration


class DirectorySecurityService:

    def __init__(self):
        self.root_directory = StorageConfiguration.ROOT_DIRECTORY.resolve()

    def resolve_safe_file_path(self, requested_filename: str) -> Path:
        resolved_path = self.root_directory / requested_filename
        resolved_path = resolved_path.resolve()
        if not str(resolved_path).startswith(str(self.root_directory)):
            raise PermissionError("Access outside root directory is not allowed")
        return resolved_path

    def validate_file_exists(self, requested_filename: str) -> Path:
        file_path = self.resolve_safe_file_path(requested_filename)
        if not file_path.exists():
            raise FileNotFoundError("Requested file does not exist")
        return file_path
