# Secure File Transfer System  
Computer Security Project – Milestones 1–5

## Team Members
- Jordi  
- Andrew  
- Manny  
- Priyanshi  

This project implements a secure file transfer system using TCP sockets, AES-256-CBC encryption, and SHA-256 integrity verification.  
The client encrypts and sends a file, and the server verifies and decrypts it before saving.

---

## Project Summary

The goal of this project was to build a custom secure file-transfer protocol over a client–server architecture.  
The final system supports:

- TCP connection between client and server  
- AES-256-CBC encryption for confidentiality  
- SHA-256 hashing for integrity  
- Transfer of filenames, encrypted bytes, and digests  
- Safe reconstruction and storage of plaintext on the server  

---

## Milestone Breakdown and Contributions

### Milestone 1 – Basic TCP Networking  
**Completed by:** Jordi  
- Created the initial TCP client and server.  
- Implemented socket creation, binding, listening, accepting, and connecting.  
- Verified basic send/receive functionality.

### Milestone 2 – Protocol Design  
**Completed by:** Manny and Priyanshi  
- Designed the message structure for filename, sizes, and data.  
- Defined how the server and client communicate in sequence.  
- Ensured compatibility for later encryption steps.

### Milestone 3 – Encryption and Decryption Logic  
**Completed by:** Andrew  
- Implemented AES encryption logic in Python.  
- Added padding and secure block operations.  
- Tested encrypted transmission and decryption with static data.

### Milestone 4 – Integrity Verification  
**Completed by:** Manny and Priyanshi  
- Added SHA-256 hashing to detect corruption or tampering.  
- Implemented digest creation on the client and verification on the server.  
- Ensured correct byte ordering and comparison.

### Milestone 5 – Full C++ Secure Transfer Implementation and Documentation
**Completed by:** Jordi  
- Rebuilt the system in C++ using OpenSSL.  
- Implemented AES-256-CBC encryption and decryption using EVP.  
- Added SHA-256 digest generation and verification.  
- Built complete send–receive protocol including:  
  - Filename  
  - Encrypted size  
  - SHA-256 digest  
  - Encrypted file bytes  
- Server validates integrity before decrypting and saving file.  
- Output stored in `received/` directory.

---

## How the Final System Works

### Client Steps
1. Reads the file from disk.  
2. Encrypts the file using AES-256-CBC.  
3. Generates a SHA-256 digest of the encrypted data.  
4. Sends:
   - Filename length  
   - Filename  
   - Encrypted file size  
   - SHA-256 digest  
   - Encrypted bytes  
5. Closes the connection.

### Server Steps
1. Accepts client connection.  
2. Receives filename and encrypted size.  
3. Receives SHA-256 digest.  
4. Receives encrypted bytes.  
5. Computes SHA-256 digest locally.  
6. Compares digests:
   - If mismatch → integrity failure  
   - If match → decrypts the file  
7. Saves plaintext into `received/filename`.  

---

## Dependencies
- OpenSSL development libraries  
- C++ compiler (g++)  
- Linux or macOS environment  

---

## Running the System

### Start Server
