const crypto = require('crypto');

function convertPublicKey(rsaPublicKey) {
    const key = crypto.createPublicKey({
        key: rsaPublicKey,
        format: 'pem',
        type: 'spki'
    });

    return key.export({
        type: 'spki',
        format: 'pem'
    }).toString();
}

module.exports = { convertPublicKey };
