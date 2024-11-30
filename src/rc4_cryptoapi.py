import functools
import io
import logging
from hashlib import sha1
from struct import pack

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def _makekey(password, salt, keyLength, block, algIdHash=0x00008004):
    r"""
    Trả về khóa trung gian.
    """
    password = password.encode("UTF-16LE")
    h0 = sha1(salt + password).digest()
    blockbytes = pack("<I", block)
    hfinal = sha1(h0 + blockbytes).digest()
    if keyLength == 40:
        key = hfinal[:5] + b"\x00" * 11
    else:
        key = hfinal[: keyLength // 8]
    return key

class RC4:
    def __init__(self, key):
        self.key = key
        self.state = list(range(256))  # Initialize the state array (S-box)
        self.i = 0
        self.j = 0
        # KSA (Key Scheduling Algorithm)
        key_length = len(key)
        j = 0
        for i in range(256):
            j = (j + self.state[i] + key[i % key_length]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]
    
    def _next_byte(self):
        # Pseudo-random byte generation using the PRGA (Pseudo-Random Generation Algorithm)
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.state[self.i]) % 256
        self.state[self.i], self.state[self.j] = self.state[self.j], self.state[self.i]
        return self.state[(self.state[self.i] + self.state[self.j]) % 256]
    
    def decrypt(self, data):
        return bytes([b ^ self._next_byte() for b in data])

class DocumentRC4CryptoAPI:
    def __init__(self):
        pass

    @staticmethod
    def verifypw(password, salt, keySize, encryptedVerifier, encryptedVerifierHash, algId=0x00006801, block=0):
        r"""
        Trả về True nếu mật khẩu đã cho là hợp lệ.
        """
        key = _makekey(password, salt, keySize, block)
        rc4 = RC4(key)
        verifier = rc4.decrypt(encryptedVerifier)
        verifierHash = rc4.decrypt(encryptedVerifierHash)
        hash = sha1(verifier).digest()
        logging.debug([verifierHash, hash])
        return hash == verifierHash

    @staticmethod
    def decrypt(password, salt, keySize, ibuf, blocksize=0x200, block=0):
        r"""
        Trả về dữ liệu đã giải mã.
        """
        obuf = io.BytesIO()

        key = _makekey(password, salt, keySize, block)
        rc4 = RC4(key)

        for buf in iter(functools.partial(ibuf.read, blocksize), b""):
            dec = rc4.decrypt(buf)
            obuf.write(dec)

            # Rekey (RC4 rekeying step)
            block += 1
            key = _makekey(password, salt, keySize, block)
            rc4 = RC4(key)  # Update RC4 state with the new key

        obuf.seek(0)
        return obuf
