FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip \
	g++ \
	make \
	libssl-dev \
	openssl \
	iproute2 \
	net-tools \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install cryptography

WORKDIR /app
COPY . .

RUN g++ server.cpp -o server -lssl -lcrypto
RUN g++ client.cpp -o client -lssl -lcrypto

CMD ["/bin/bash"]
