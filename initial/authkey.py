from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    with open("initial/key.key", "wb") as key_file:
        key_file.write(key)

# Function to load key
def load_key():
    if os.path.exists("initial/key.key"):
        with open("initial/key.key", "rb") as key_file:
            key = key_file.read()
        return key
    else:
        print("Key file not found. Generating new key.")
        generate_key()
        return load_key()

auth_key = load_key()