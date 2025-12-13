#include <iostream>
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/aes.h>
#include <string>
#include <vector>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace std;

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

vector<unsigned char> decryptAES(const vector<unsigned char>& cText,const unsigned char key[32],
                                 const unsigned char iv[16]);

int main() {

    int server_create = socket(AF_INET, SOCK_STREAM, 0);
    if (server_create < 0) {
        cerr << "socket creation failed\n";
        return 1;
    }

    sockaddr_in server_addr{};
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(6767);

    if (::bind(server_create, (sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        cerr << "bind failed\n";
        return 1;
    }

    if (listen(server_create, 1) < 0) {
        cerr << "listen failed\n";
        return 1;
    }
    cout << "Server listening on 6767...\n";
    cout << "Secure drop waiting for incoming file: " << endl;

    sockaddr_in client_addr{};
    socklen_t client_len = sizeof(client_addr);
    int client_create = accept(server_create,(sockaddr*)&client_addr,&client_len);
    if (client_create < 0) {
        cerr << "accept failed\n";
        return 1;
    }

    cout << "Client connected.\n";

    // get filename
    int flen = 0;
    recv(client_create, &flen, sizeof(flen), 0);

    vector<char> fname(flen+1);
    recv(client_create, fname.data(), flen, 0);
    fname[flen] = '\0';

    cout << "Filename: " << fname.data() << endl;

    // get enc size
    long encSize = 0;
    recv(client_create, &encSize, sizeof(encSize), 0);
    cout << "Encrypted size: " << encSize << endl;

    // get enc bytes
    vector<unsigned char> cText(encSize);
    long total = 0;
    while (total < encSize) {
    int bytes = recv(client_create, cText.data() + total, encSize - total, 0);
    if (bytes < 0) {
        cerr << "recv failed\n";
        return 1;
    }
        if (bytes == 0) break;
        total += bytes;
    }

    if (total != encSize) cerr << "Did not receive full encrypted file" << endl;


    unsigned char recvDigest[32];
    recv(client_create, recvDigest, 32, 0);

    unsigned char calcDigest[32];
    EVP_Digest(cText.data(), cText.size(), calcDigest, NULL, EVP_sha256(), NULL);

    // compare
    if (memcmp(recvDigest, calcDigest, 32) != 0) {
        cerr << "Integrity check failed file has been corrupted" << endl;
        return 1;
    }

    cout << "integritt check ahs passed\n";

    //decrypt
    vector<unsigned char> pText = decryptAES(cText, key, iv);
    cout << "Decrypted size: " << pText.size() << endl;

    // save output
    system("mkdir -p received");

    string outPath = "received/" + string(fname.data());
    FILE* out = fopen(outPath.c_str(), "wb");
    if (!out){
        cerr << "could not create output file\n";
        return 1;
    }

    fwrite(pText.data(), 1, pText.size(), out);
    fclose(out);

    cout << "File saved to: " << outPath << endl;

    close(client_create);
    close(server_create);
    return 0;
}

vector<unsigned char> decryptAES(const vector<unsigned char>& cText, const unsigned char key[32],
                                 const unsigned char iv[16]) {
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv);

    vector<unsigned char> pText(cText.size() + 32);

    int length = 0;
    EVP_DecryptUpdate(ctx, pText.data(), &length, cText.data(), cText.size());

    int length2 = 0;
    EVP_DecryptFinal_ex(ctx, pText.data() + length, &length2);

    pText.resize(length + length2);
    EVP_CIPHER_CTX_free(ctx);

    return pText;
}
