
import json
from getpass import getpass
from nacl.exceptions import CryptoError
import nacl.secret
import nacl.utils
import nacl.pwhash
from pathlib import Path

from .exceptions import PasswordError

class FileDecryptor:

    def __init__(self):
        self.vault = 'webweaver/client.bin'
        self.file_path = Path(self.vault)
        if not self.file_path.exists():
            raise FileNotFoundError("client.bin does not exist in the specified directory!")


    def decrypt_data(self, encrypted_data:bytes, password:str) -> dict:
        # Extract salt and encrypted part
        salt = encrypted_data[:nacl.pwhash.argon2i.SALTBYTES]
        encrypted_part = encrypted_data[nacl.pwhash.argon2i.SALTBYTES:]

        # Derive key from password and salt
        key = nacl.pwhash.argon2i.kdf(
            nacl.secret.SecretBox.KEY_SIZE, password.encode(), salt,
            opslimit=nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE,
            memlimit=nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE
        )

        # Decrypt
        box = nacl.secret.SecretBox(key)
        decrypted_data = box.decrypt(encrypted_part)

        return json.loads(decrypted_data.decode())


    def decrypt(self) -> dict:
        with open(self.vault, "rb") as f:
            stored_encrypted_data = f.read()
        password = getpass(">> Enter your password: ")
        try:
            decrypted_data = self.decrypt_data(stored_encrypted_data, password)
        except CryptoError:
            raise PasswordError
        return decrypted_data
    

# if __name__ == '__main__':
#     pass
