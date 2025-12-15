CERT_DIR=certs

.PHONY: all ca server client clean

all: ca server client

ca:
	mkdir -p $(CERT_DIR)
	openssl genrsa -out $(CERT_DIR)/ca.key 4096
	openssl req -x509 -new -nodes -key $(CERT_DIR)/ca.key -sha256 -days 365 \
		-subj "/C=US/ST=MA/L=Lowell/O=SecureDrop/OU=CA/CN=SecureDropCA" \
		-out $(CERT_DIR)/ca.crt
	echo 1000 > $(CERT_DIR)/ca.srl

server:
	openssl genrsa -out $(CERT_DIR)/server.key 2048
	openssl req -new -key $(CERT_DIR)/server.key \
		-subj "/C=US/ST=MA/L=Lowell/O=SecureDrop/OU=Server/CN=server" \
		-out $(CERT_DIR)/server.csr
	openssl x509 -req -in $(CERT_DIR)/server.csr \
		-CA $(CERT_DIR)/ca.crt -CAkey $(CERT_DIR)/ca.key \
		-CAserial $(CERT_DIR)/ca.srl \
		-out $(CERT_DIR)/server.crt -days 365 -sha256

client:
	openssl genrsa -out $(CERT_DIR)/client.key 2048
	openssl req -new -key $(CERT_DIR)/client.key \
		-subj "/C=US/ST=MA/L=Lowell/O=SecureDrop/OU=Client/CN=client" \
		-out $(CERT_DIR)/client.csr
	openssl x509 -req -in $(CERT_DIR)/client.csr \
		-CA $(CERT_DIR)/ca.crt -CAkey $(CERT_DIR)/ca.key \
		-CAserial $(CERT_DIR)/ca.srl \
		-out $(CERT_DIR)/client.crt -days 365 -sha256

clean:
	rm -rf $(CERT_DIR)
