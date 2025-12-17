#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/aes.h>
#include <iostream>
#include <vector>
#include <string>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace std; using std::vector;

unsigned char key[32] = {
    1,2,3,4,5,6,7,8,
    9,10,11,12,13,14,15,16,
    17,18,19,20,21,22,23,24,
    25,26,27,28,29,30,31,32
};

unsigned char iv[16] = {
    11,22,33,44,55,66,77,88,
    99,111,122,133,144,155,166,177
};

vector<unsigned char> encryptAES(const vector<unsigned char>& pText, const unsigned char key[32],
                                const unsigned char iv[16]);
int main(int argc, char* argv[]) {

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "socket creation has failed" << endl;
        return 1;
    }

    // open file(update to integrate cpp to python milestones 1-4)
    if (argc != 3) {
        std::cerr << "usign: ./cliet <server_ip> <filename>" << endl;
        return 1;
    }
    const char* server_ip = argv[1];
    const char* filename = argv[2];

    FILE* fp = fopen(filename, "rb");
    if(!fp) {
        std::cerr << "error could not open the file" << endl;
        return 1;
    }

    // get size of file
    fseek(fp, 0, SEEK_END);
    long fileSize = ftell(fp);
    fseek(fp, 0, SEEK_SET);

    cout << "file size is: " << fileSize << "bytes" << endl;



    // connect to port
    sockaddr_in server_addr{};
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(6767);
    inet_pton(AF_INET, server_ip, &server_addr.sin_addr);

    if(connect(sock, (sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "connection has failed" << endl;
        return 1;
    }
    // send teh filename
    int flen = strlen(filename);
    send(sock, &flen, sizeof(flen), 0);
    send(sock, filename, flen, 0);

    vector<unsigned char>pText(fileSize);
    fread(pText.data(), 1, fileSize, fp);
    fclose(fp);

    // encrypt file
    vector<unsigned char> cText = encryptAES(pText, key, iv);

    long encryptSize = cText.size();
    send(sock, &encryptSize, sizeof(encryptSize), 0);

    // send encrypted data first
    send(sock, cText.data(), encryptSize, 0);

    // now compute and send digest
    unsigned char digest[32];
    EVP_Digest(cText.data(), cText.size(), digest, NULL, EVP_sha256(), NULL);
    send(sock, digest, 32, 0);

    close(sock);

    return 0;
}

vector<unsigned char> encryptAES(const vector<unsigned char>& pText, const unsigned char key[32],
                                const unsigned char iv[16]){
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv);

    vector<unsigned char> cipherText(pText.size() + 16);
    int length = 0;
    EVP_EncryptUpdate(ctx, cipherText.data(), &length, pText.data(), pText.size());

    int length2 = 0;
    EVP_EncryptFinal_ex(ctx, cipherText.data() + length, &length2);
    cipherText.resize(length + length2);
    EVP_CIPHER_CTX_free(ctx);

    return cipherText;
}
