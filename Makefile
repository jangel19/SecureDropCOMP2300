CXX = g++
CXXFLAGS = -std=c++17 -Wall
OPENSSL_INC = -I/opt/homebrew/opt/openssl@3/include
OPENSSL_LIB = -L/opt/homebrew/opt/openssl@3/lib -lssl -lcrypto

CLIENT = client
SERVER = server

all: $(CLIENT) $(SERVER)

$(CLIENT): client.cpp
	$(CXX) $(CXXFLAGS) client.cpp -o $(CLIENT) $(OPENSSL_INC) $(OPENSSL_LIB)

$(SERVER): server.cpp
	$(CXX) $(CXXFLAGS) server.cpp -o $(SERVER) $(OPENSSL_INC) $(OPENSSL_LIB)

run: all
	@echo "[+] Starting SecureDrop server..."
	./server &
	@sleep 1
	@echo "[+] Starting SecureDrop interface..."
	python3 secure_drop.py

clean:
	rm -f $(CLIENT) $(SERVER)
