import os, struct
from tls import create_secure_server

HOST = "0.0.0.0"
PORT = 8443

CERT = "certs/server.crt"
KEY  = "certs/server.key"
CA   = "certs/ca.crt"

def main():
    server = create_secure_server(HOST, PORT, CERT, KEY, CA)
    print("Secure server listening on port 8443")

    conn, addr = server.accept()
    print(f"Secure connection from {addr}")

    seq = struct.unpack("!Q", conn.recv(8))[0]
    fname_len = struct.unpack("!I", conn.recv(4))[0]
    filename = conn.recv(fname_len).decode()
    filesize = struct.unpack("!Q", conn.recv(8))[0]

    conn.send(b"y")  # auto-accept for demo

    os.makedirs("received", exist_ok=True)
    path = os.path.join("received", filename)

    received = 0
    with open(path, "wb") as f:
        while received < filesize:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)
            received += len(data)

    print("File received securely:", path)
    conn.close()

if __name__ == "__main__":
    main()
