class FileFormatError(Exception):
    """Được ném ra khi định dạng tệp không được hỗ trợ hoặc không thể nhận dạng."""
    pass


class ParseError(Exception):
    """Được ném ra khi không thể phân tích tệp một cách chính xác."""
    pass


class DecryptionError(Exception):
    """Được ném ra khi không thể giải mã tệp."""
    pass


class EncryptionError(Exception):
    """Được ném ra khi không thể mã hóa tệp."""
    pass


class InvalidKeyError(DecryptionError):
    """Được ném ra khi mật khẩu hoặc khóa được cung cấp không đúng hoặc không thể xác minh."""
    pass
