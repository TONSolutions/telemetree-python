const crypto = require('crypto');
const { publicEncrypt, privateDecrypt } = require('crypto');

class EncryptionService {
    constructor(publicKey) {
        this.publicKey = publicKey;
    }

    rsaEncrypt(message) {
        if (typeof message !== 'string' && !Buffer.isBuffer(message)) {
            throw new Error('Message must be a string or buffer');
        }

        const bufferMessage = Buffer.isBuffer(message) ? message : Buffer.from(message, 'utf8');
        const encryptedMessage = publicEncrypt(this.publicKey, bufferMessage);
        return encryptedMessage.toString('base64');
    }

    generateAesKeyAndIv() {
        const key = crypto.randomBytes(16); // AES 128-bit key
        const iv = crypto.randomBytes(16); // AES IV
        return { key, iv };
    }

    encryptWithAes(key, iv, message) {
        if (typeof message !== 'string') {
            throw new Error('Message must be a string');
        }

        const cipher = crypto.createCipheriv('aes-128-cbc', key, iv);
        let encrypted = cipher.update(message, 'utf8', 'base64');
        encrypted += cipher.final('base64');
        return encrypted;
    }

    encrypt(message) {
        if (typeof message !== 'string') {
            throw new Error('Message must be a string');
        }

        const { key, iv } = this.generateAesKeyAndIv();

        const encryptedKey = this.rsaEncrypt(key);
        const encryptedIv = this.rsaEncrypt(iv);

        const encryptedBody = this.encryptWithAes(key, iv, message);

        return {
            key: encryptedKey,
            iv: encryptedIv,
            body: encryptedBody,
        };
    }
}

module.exports = { EncryptionService };
