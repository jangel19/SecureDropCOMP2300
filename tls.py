import socket, ssl

def create_secure_server(host, port, certfile, keyfile, ca_file):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    context.load_verify_locations(cafile=ca_file)
    context.verify_mode = ssl.CERT_REQUIRED

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    return context.wrap_socket(sock, server_side=True)
rm 

def create_secure_client(host, port, ca_file, certfile, keyfile):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    context.load_verify_locations(cafile=ca_file)

    context.load_cert_chain(
        certfile=certfile,
        keyfile=keyfile
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(sock, server_hostname=host)
    secure_sock.connect((host, port))

    return secure_sock


def analyze_connection_security(ssl_socket):
    cert = ssl_socket.getpeercert()
    return {
        "protocol": ssl_socket.version(),
        "cipher": ssl_socket.cipher(),
        "certificate_verified": cert is not None
    }
