#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <openssl/sha.h>

std::vector<unsigned char> generateKey(const std::string& password) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256(reinterpret_cast<const unsigned char*>(password.c_str()), password.size(), hash);
    std::vector<unsigned char> key(hash, hash + SHA256_DIGEST_LENGTH);
    return key;
}

std::vector<unsigned char> readFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    std::vector<unsigned char> data;
    char c;
    while (file.get(c)) {
        data.push_back(static_cast<unsigned char>(c));
    }
    return data;
}

void writeFile(const std::string& filename, const std::vector<unsigned char>& data) {
    std::ofstream file(filename, std::ios::binary);
    for (unsigned char byte : data) {
        file.put(static_cast<char>(byte));
    }
}

std::vector<unsigned char> xorEncryptDecrypt(const std::vector<unsigned char>& data, const std::vector<unsigned char>& key) {
    std::vector<unsigned char> result;
    size_t keySize = key.size();
    for (size_t i = 0; i < data.size(); ++i) {
        result.push_back(data[i] ^ key[i % keySize]);
    }
    return result;
}

void printDecryptedFile(const std::vector<unsigned char>& decryptedData) {
    for (unsigned char byte : decryptedData) {
        std::cout << byte;
    }
}

int main() {
    int choice;
    std::cout << "Entrer votre choix (1 => encrypt , 2 => Decrypt) : " ; 
    std::cin >> choice;
    std::string password;
    std::getline(std::cin, password);
    std::vector<unsigned char> key = generateKey(password);

    if (choice == 1) {
        std::vector<unsigned char> data = readFile("toConvert.txt");
        std::vector<unsigned char> encryptedData = xorEncryptDecrypt(data, key);
        writeFile("converted.txt", encryptedData);
        std::cout << "converted.txt\n";
    } else if (choice == 2) {
        std::vector<unsigned char> encryptedData = readFile("converted.txt");
        std::vector<unsigned char> decryptedData = xorEncryptDecrypt(encryptedData, key);
        printDecryptedFile(decryptedData);
    }

    return 0;
}
