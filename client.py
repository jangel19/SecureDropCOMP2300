import os
import struct
import secrets
import sys
from tls import create_secure_client, analyze_connection_security

PORT = 8443
CA_CERT = "certs/ca.crt"


def send_file(receiver_ip, filepath):
    if not os.path.exists(filepath):
        print("Error: file does not exist")
        return

    # get TLS-secured connection
    sock = create_secure_client(receiver_ip, PORT, CA_CERT)

    # print TLS details
    tls_info = analyze_connection_security(sock)
    print("TLS Info:", tls_info)

    # random sequence number
    seq = secrets.randbits(64)

    filename = os.path.basename(filepath).encode()
    filesize = os.path.getsize(filepath)

    # send metadata
    sock.sendall(struct.pack("!Q", seq))
    sock.sendall(struct.pack("!I", len(filename)))
    sock.sendall(filename)
    sock.sendall(struct.pack("!Q", filesize))

    # wait for receiver approval
    decision = sock.recv(1).decode()
    if decision != "y":
        print("Receiver rejected transfer")
        sock.close()
        return

    # send the file contents
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            sock.sendall(chunk)

    print("File sent securely")
    sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <receiver_ip> <filename>")
        sys.exit(1)

    receiver_ip = sys.argv[1]
    filename = sys.argv[2]

    send_file(receiver_ip, filename)
