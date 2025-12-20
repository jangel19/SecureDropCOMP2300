# SecureDrop – Secure File Transfer System  
**Computer Security Project (Milestones 1–5)**

## Team Members
- **Jordi Lopez**
- Manny  
- Priyanshi  
- Andrew  

---

## Project Overview

SecureDrop is a secure file transfer system developed for a Computer Security course.  
The project implements a **custom client–server protocol over TCP**, with cryptographic protections to ensure confidentiality and integrity during file transfers.

The final working system was implemented primarily in **C++ using OpenSSL**, with a **Python-based SecureDrop interface** used for user registration, login, contact management, and orchestration.

While Python was explored for cryptographic communication, the final secure transfer layer was implemented in C++ for stability, control, and reliability under deadline constraints.

---

## Security Features

- **AES-256-CBC encryption** for file confidentiality  
- **SHA-256 hashing** for integrity verification  
- **Explicit protocol design** for structured communication  
- **TCP sockets** for reliable transport  
- **Containerized testing** to simulate multiple machines  

---

## Milestone Breakdown and Contributions

### Milestone 1 – User Registration & Authentication  
**Primary contributor:** Jordi  
**Bug fixes:** Priyanshi  

- Implemented user registration and login in Python  
- Used salted SHA-256 hashing for password storage  
- Stored user data in structured JSON format  
- Fixed bugs related to empty database initialization  

---

### Milestones 2 & 3 – Protocol Design and Cryptography  
**Contributors:** Priyanshi

- Designed the message structure for file transfer  
- Defined sequencing for filenames, sizes, and encrypted data  
- Initial cryptography experiments were implemented in Python  

---

### Milestone 4 – Network Discovery  
**Contributor:** Manny  
**Debugging & Integration:** Jordi  

- Implemented network discovery and handshake logic  
- Jordi debugged handshake failures, JSON parsing errors, and network edge cases  
- Integrated discovery logic into the SecureDrop shell  

---

### Milestone 5 – Final Secure File Transfer (C++)  
**Completed by:** Jordi  

This milestone represents the final, fully functional system.

- Reimplemented the secure file transfer layer entirely in **C++**
- Used **OpenSSL EVP APIs** for AES-256-CBC encryption and decryption
- Implemented SHA-256 digest generation and verification
- Designed a complete transfer protocol including:
  - Filename and filename length
  - Encrypted file size
  - Encrypted file bytes
  - SHA-256 digest
- Server verifies integrity before decrypting
- Decrypted files are safely written to the `received/` directory
- Updated the server to handle **multiple transfers without restarting**
- Fixed Python-to-C++ integration issues involving IPs and ports
- Integrated automatic server startup into SecureDrop
- Set up and tested the system across **multiple Docker containers**
- Completed final debugging, integration, and demo preparation independently

---

## Why C++ Was Used for the Final System

Python was initially explored for TLS-style certificate-based encryption.  
However, during development the team encountered:

- TLS handshake failures  
- Certificate verification errors  
- DNS and hostname mismatches  
- Dependency and environment inconsistencies across containers  

To ensure a reliable and debuggable final demo, the project pivoted to a **C++ OpenSSL-based implementation**, which provided:

- Lower-level control over sockets and cryptography  
- Predictable behavior across environments  
- Easier debugging of byte-level protocol issues  

---

## Known Limitations & Security Considerations

- AES keys and IVs are statically defined (not suitable for production)
- No perfect forward secrecy
- No replay attack protection
- No certificate-based authentication in the final C++ system

**Potential future improvements**:
- TLS with proper certificate management
- Dynamic key exchange (Diffie–Hellman)
- Mutual authentication
- Replay protection and session management

---

## Dependencies

- OpenSSL development libraries  
- g++ compiler  
- Linux or macOS environment  
- Docker (used for multi-container testing)

---

## Final Notes

Despite coordination challenges, this project was a valuable learning experience.  
The final system demonstrates practical applications of cryptography, networking, debugging, and system integration under real constraints.

The project strengthened skills in:
- Encryption and integrity verification
- Networking and sockets
- Linux systems
- Debugging distributed applications
- Containerized testing and deployment

---

**Author & Team Lead:** Jordi Lopez
