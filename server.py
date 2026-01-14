import socket
import threading

server = socket.socket()
server.bind(("localhost", 9999))
server.listen(2)

print("Server running...")

c1, _ = server.accept()
print("Client 1 connected")

c2, _ = server.accept()
print("Client 2 connected")

# Exchange public keys
pub1 = c1.recv(2048)
c2.send(pub1)

pub2 = c2.recv(2048)
c1.send(pub2)

# Forward messages both ways
def forward(sender, receiver):
    while True:
        try:
            data = sender.recv(4096)
            if not data:
                break
            receiver.send(data)
        except:
            break

threading.Thread(target=forward, args=(c1, c2)).start()
threading.Thread(target=forward, args=(c2, c1)).start()
