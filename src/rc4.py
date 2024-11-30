import io
import logging
from hashlib import md5
from struct import pack

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _makekey(password, salt, block):
    r"""
    Trả về một khóa trung gian.

        >>> password = 'password1'
        >>> salt = b'\xe8w,\x1d\x91\xc5j7\x96Ga\xb2\x80\x182\x17'
        >>> block = 0
        >>> expected = b' \xbf2\xdd\xf5@\x85\x8cQ7D\xaf\x0f$\xe0<'
        >>> _makekey(password, salt, block) == expected
        True
    """
    # https://msdn.microsoft.com/en-us/library/dd920360(v=office.12).aspx
    password = password.encode("UTF-16LE")
    h0 = md5(password).digest()
    truncatedHash = h0[:5]
    intermediateBuffer = (truncatedHash + salt) * 16
    h1 = md5(intermediateBuffer).digest()
    truncatedHash = h1[:5]
    blockbytes = pack("<I", block)
    hfinal = md5(truncatedHash + blockbytes).digest()
    key = hfinal[: 128 // 8]
    return key


def rc4(key, data):
    """
    Thực hiện mã hóa/giải mã RC4.
    """
    # KSA: Khởi tạo bộ trạng thái S với khóa
    key_length = len(key)
    S = list(range(256))  # Mảng S chứa 256 giá trị
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA: Tạo dòng khóa từ mảng S
    i = 0
    j = 0
    output = bytearray()

    # Tạo dòng khóa và XOR với dữ liệu
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]  # Tạo byte khóa
        output.append(byte ^ K)  # XOR giữa byte dữ liệu và byte khóa

    return bytes(output)


class DocumentRC4:
    def __init__(self):
        pass

    @staticmethod
    def verifypw(password, salt, encryptedVerifier, encryptedVerifierHash):
        r"""
        Trả về True nếu mật khẩu đã cho là hợp lệ.

            >>> password = 'password1'
            >>> salt = b'\xe8w,\x1d\x91\xc5j7\x96Ga\xb2\x80\x182\x17'
            >>> encryptedVerifier = b'\xc9\xe9\x97\xd4T\x97=1\x0b\xb1\xbap\x14&\x83~'
            >>> encryptedVerifierHash = b'\xb1\xde\x17\x8f\x07\xe9\x89\xc4M\xae^L\xf9j\xc4\x07'
            >>> DocumentRC4.verifypw(password, salt, encryptedVerifier, encryptedVerifierHash)
            True
        """
        block = 0
        key = _makekey(password, salt, block)

        # Giải mã dữ liệu bằng RC4
        verifier = rc4(key, encryptedVerifier)

        # Tính toán hash MD5 của dữ liệu đã giải mã
        hash = md5(verifier).digest()

        # So sánh hash đã giải mã với hash được cung cấp
        return hash == encryptedVerifierHash

    @staticmethod
    def decrypt(password, salt, ibuf, blocksize=0x200):
        r"""
        Trả về dữ liệu đã giải mã.
        """
        obuf = io.BytesIO()

        block = 0
        key = _makekey(password, salt, block)

        while True:
            buf = ibuf.read(blocksize)
            if not buf:
                break

            # Giải mã khối dữ liệu bằng RC4
            dec = rc4(key, buf)

            # Viết dữ liệu giải mã vào bộ đệm
            obuf.write(dec)

            # Tăng block và tái tạo lại khóa
            block += 1
            key = _makekey(password, salt, block)

        obuf.seek(0)
        return obuf
