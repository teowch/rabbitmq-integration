from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

public_key = private_key.public_key()
with open("public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

def create_key_pair(pk_filename, pub_filename):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    if not os.path.exists("./keys/" + pk_filename + ".pem"):
        with open("./keys/" + pk_filename + ".pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

    if not os.path.exists("./keys/" + pub_filename + ".pem"):
        public_key = private_key.public_key()
        with open("./keys/" + pub_filename + ".pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))