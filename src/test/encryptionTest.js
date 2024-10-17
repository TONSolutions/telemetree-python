const { expect } = require('chai');
const crypto = require('crypto');
const { publicEncrypt, privateDecrypt } = require('crypto');
const { EncryptionService } = require('../telemetree/encryption');

const generateKeyPair = () => {
    const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
        modulusLength: 2048,
    });
    return { publicKey, privateKey };
};

const { publicKey, privateKey } = generateKeyPair();
const encryptionService = new EncryptionService(publicKey.export({ type: 'pkcs1', format: 'pem' }));

describe('EncryptionService', () => {
    describe('rsaEncrypt', () => {
        it('should encrypt a message using RSA', () => {
            const message = 'Hello, world!';
            const encryptedMessage = encryptionService.rsaEncrypt(message);
            const decryptedMessage = privateDecrypt(privateKey, Buffer.from(encryptedMessage, 'base64')).toString('utf8');
            expect(decryptedMessage).to.equal(message);
        });
    });

    describe('generateAesKeyAndIv', () => {
        it('should generate a 128-bit AES key and IV', () => {
            const { key, iv } = encryptionService.generateAesKeyAndIv();
            expect(key).to.have.lengthOf(16);
            expect(iv).to.have.lengthOf(16);
        });
    });

    describe('encryptWithAes', () => {
        it('should encrypt a message using AES', () => {
            const { key, iv } = encryptionService.generateAesKeyAndIv();
            const message = 'Hello, world!';
            const encryptedMessage = encryptionService.encryptWithAes(key, iv, message);
            const decipher = crypto.createDecipheriv('aes-128-cbc', key, iv);
            let decryptedMessage = decipher.update(encryptedMessage, 'base64', 'utf8');
            decryptedMessage += decipher.final('utf8');
            expect(decryptedMessage).to.equal(message);
        });
    });

    describe('encrypt', () => {
        it('should encrypt a message using RSA and AES', () => {
            const message = 'Hello, world!';
            const encryptedData = encryptionService.encrypt(message);
            const decryptedKey = privateDecrypt(privateKey, Buffer.from(encryptedData.key, 'base64'));
            const decryptedIv = privateDecrypt(privateKey, Buffer.from(encryptedData.iv, 'base64'));
            const decipher = crypto.createDecipheriv('aes-128-cbc', decryptedKey, decryptedIv);
            let decryptedMessage = decipher.update(encryptedData.body, 'base64', 'utf8');
            decryptedMessage += decipher.final('utf8');
            expect(decryptedMessage).to.equal(message);
        });
    });
});
