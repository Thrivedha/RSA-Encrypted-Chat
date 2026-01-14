import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# Generate RSA keys
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Connect to server
s = socket.socket()
s.connect(("localhost", 9999))

# Send public key
s.send(public_pem)

# Receive friend's public key
friend_pub = s.recv(2048)
friend_key = serialization.load_pem_public_key(friend_pub)

print("Secure connection established")

# Receive messages
def receive():
    while True:
        try:
            data = s.recv(4096)
            msg = private_key.decrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print("\nFriend:", msg.decode())
        except:
            break

threading.Thread(target=receive).start()

# Send messages
while True:
    text = input()
    if text.lower()=="exit":
        s.close()
        break
    encrypted = friend_key.encrypt(
        text.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    s.send(encrypted)
