import struct
import secrets
import hashlib
from typing import Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class AES:
    IV_SIZE = 16
    AES_BLOCKSIZE = 32

    def __entropy__(self, n: int) -> bytes:
        return secrets.token_bytes(n)

    def __pack__(self, size: int, iv: bytes, body: bytes) -> bytes:
        return struct.pack("<I", size) + iv + body

    def __unpack__(self, raw: bytes) -> Tuple[int, bytes, bytes]:
        isize = struct.calcsize('I')
        size = struct.unpack("<I", raw[:isize])[0]
        iv = raw[isize:isize + AES.IV_SIZE]
        body = raw[isize + AES.IV_SIZE:]

        return size, iv, body

    def __pad__(self, plaintext: bytes) -> bytes:
        if len(plaintext) % AES.AES_BLOCKSIZE != 0:
            plaintext += b'0' * (AES.AES_BLOCKSIZE - len(plaintext) % AES.AES_BLOCKSIZE)

        return plaintext

    def key_rand(self):
        return self.__entropy__(AES.AES_BLOCKSIZE)

    def key_pbkdf2(self, password: bytes, iterations: int = 65536) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=AES.AES_BLOCKSIZE,
            salt=hashlib.sha256(password).digest(),
            iterations=iterations,
        )

        return kdf.derive(password)

    def encrypt(self, key: bytes, plaintext: bytes) -> Tuple[bytes, bytes]:
        iv = self.__entropy__(AES.IV_SIZE)
        padded = self.__pad__(plaintext)

        encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()

        return self.__pack__(len(plaintext), iv, ciphertext)

    def decrypt(self, key: bytes, ciphertext: bytes) -> bytes:
        size, iv, body = self.__unpack__(ciphertext)

        decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()

        plaintext = decryptor.update(body) + decryptor.finalize()

        return plaintext[:size]
