from cryptography.fernet import Fernet
import os

# Function to generate and save key
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Function to load key
def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            key = key_file.read()
        return key
    else:
        print("Key file not found. Generating new key.")
        generate_key()
        return load_key()

# Load or generate key
key = load_key()

# Use the key for encryption/decryption
cipher_suite = Fernet(key)

# Encrypt a message
message = "Sensitive information"
encrypted_message = cipher_suite.encrypt(message.encode())
print("Encrypted message:", encrypted_message)

# Decrypt the message
decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
print("Decrypted message:", decrypted_message)