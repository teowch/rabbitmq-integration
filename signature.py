import pika
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


def get_private_key(pk_filename):
    with open("./keys/" + pk_filename + ".pem", "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

def get_public_key(pub_filename):
    with open("./keys/" + pub_filename + ".pem", "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

def sign_message(message, private_key):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read())

def verify_message(message, signature, public_key):
    try:
        public_key.verify(
            bytes.fromhex(signature),
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Falha na verificação da assinatura: {e}")
        return False