import forge from 'node-forge';

export class AsymmCrypto {
    constructor(publicKey) {
        this.publicKey = publicKey;
        if(!this.publicKey.includes("-----BEGIN PUBLIC KEY-----")){
            this.publicKey = "-----BEGIN PUBLIC KEY-----" + this.publicKey + "-----END PUBLIC KEY-----";
        }
        this.publicCrypto = forge.pki.publicKeyFromPem(this.publicKey);
    }

    encrypt(input, padding = true){
        const encryptData = this.publicCrypto.encrypt(input, 'RSA-OAEP', {
            md: forge.md.sha256.create(),
            mgf1: {
                md: forge.md.sha256.create()
            }
        });
        return forge.util.encode64(encryptData);
    }
}

export class SymmCrypto {
    constructor() {
        this.ivSize = 128;
        this.saltSize = 128;
        this.generateSecret();
    }

    encrypt(input, secret = this.getKeyIv()) {
        const key = secret.key;
        const iv = secret.iv;
        const additionalData = secret.additionalData
        let cipher = forge.cipher.createCipher('AES-GCM', key);
        cipher.start({iv: iv, additionalData:additionalData});
        cipher.update(forge.util.createBuffer(input, 'utf8'));
        cipher.finish();
        return JSON.stringify({
            payload: forge.util.encode64(cipher.output.getBytes()),
            tag: forge.util.encode64(cipher.mode.tag.getBytes())
        })
    }

    decrypt(input, secret = this.getKeyIv()) {
        const key = secret.key
        const iv = secret.iv
        const additionalData = secret.additionalData
        const tag = forge.util.createBuffer(forge.util.decode64(input.tag))
        let deCipher = forge.cipher.createDecipher('AES-GCM', key);
        deCipher.start({
            iv: iv,
            tag: tag,
            tagLength: 128
        });
        deCipher.update(forge.util.createBuffer(forge.util.decode64(input.payload)));
        deCipher.finish();
        return forge.util.decodeUtf8(deCipher.output.getBytes());
    }

    getKeyIv() {
        return {
            key: this.key,
            iv: this.iv,
            additionalData: this.additionalData
        }
    }

    getKeyIvForSending(){
        return {
            key: forge.util.encode64(this.key),
            iv: forge.util.encode64(this.iv),
            additionalData: forge.util.encode64(this.additionalData)
        }
    }

    generateSecret(password = '') {
        this.additionalData = forge.random.getBytesSync(this.saltSize / 8)
        const salt = forge.random.getBytesSync(this.saltSize / 8);
        const secret = `${password}${window.crypto.getRandomValues(new Uint32Array(1))[0]}`.substring(0, 128);
        this.iv = forge.random.getBytesSync(this.ivSize / 8);
        this.key = forge.pkcs5.pbkdf2(secret, salt, 1000, 32);
    }

}