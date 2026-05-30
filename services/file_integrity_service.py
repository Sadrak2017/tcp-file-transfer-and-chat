from utils.sha256_calculator import Sha256Calculator


class FileIntegrityService:
    def __init__(self):
        self.sha256_calculator = Sha256Calculator()

    def calculate_file_sha256(self, file_path) -> str:
        return self.sha256_calculator.calculate_file_sha256(file_path)

    def validate_file_integrity(self, file_path, expected_sha256: str) -> bool:
        calculated_sha256 = self.calculate_file_sha256(file_path)
        return calculated_sha256 == expected_sha256
