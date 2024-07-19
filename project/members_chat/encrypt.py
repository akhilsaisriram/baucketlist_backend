from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode
from os import urandom

def key_from_string(key_str):
    # Remove dashes and convert to bytes
    key_hex = key_str.replace('-', '')
    return bytes.fromhex(key_hex)

def encrypt_data(key_str, data):
    key = key_from_string(key_str)

    # Generate a random IV (Initialization Vector)
    iv = urandom(16)

    # Pad the data to match the block size of the encryption algorithm
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Create a Cipher object using AES algorithm, CBC mode, and the generated IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Encrypt the padded data
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Combine IV and encrypted data into a single byte string
    encrypted_message = iv + encrypted_data

    # Base64 encode the encrypted message for easier storage or transmission
    encrypted_base64 = b64encode(encrypted_message).decode('utf-8')

    return encrypted_base64

def decrypt_data(key_str, encrypted_base64):
    key = key_from_string(key_str)

    # Base64 decode the encrypted message
    encrypted_message = b64decode(encrypted_base64)

    # Extract IV and encrypted data
    iv = encrypted_message[:16]
    encrypted_data = encrypted_message[16:]

    # Create a Cipher object using AES algorithm, CBC mode, and the extracted IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Decrypt the encrypted data
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data
