import pRetry from 'p-retry';
import {AsymmCrypto, SymmCrypto} from "./Crypto";
import {BACKEND_URL} from "../Constants/Constants"

class HttpService {
    constructor(){
        this.getFetch(BACKEND_URL + '/rsa_pub')
        .then((responseData) => {
            this.publicKey = responseData.Data
            this.asymmCrypto = new AsymmCrypto(this.publicKey)
            this.symmCrypto = new SymmCrypto()
        })
    }

    setToken(token){
        this.token = token
        this.myHeaders = new Headers({
                'Authorization': `Bearer ${this.token}`,
                'Content-Type':  "application/json"
            });
    }

    decrypt(msg){
        return this.symmCrypto.decrypt(JSON.parse(msg))
    }

    async getRun(url){
        const response = await fetch(url,
                                    {method:'get',
                                    headers: this.myHeaders});

        // Abort retrying if the resource doesn't exist
        if (response.status === 404) {
            throw new pRetry.AbortError(response.statusText);
        } else if (response.status === 401){
            // Handle fetching new token
        }
        return response.json();
    }

    async postRun(url, body){
        let payload = {}
        payload.payload = this.symmCrypto.encrypt(JSON.stringify(body))
        payload.route = this.symmCrypto.encrypt(url)
        payload.secret = this.asymmCrypto.encrypt(JSON.stringify(this.symmCrypto.getKeyIvForSending()))
        const response = await fetch(BACKEND_URL, 
                                {method: 'post', 
                                headers: this.myHeaders,
                                body: JSON.stringify(payload)});
        // Abort retrying if the resource doesn't exist
        if (response.status === 404) {
            throw new pRetry.AbortError(response.statusText);
        } else if (response.status === 401){
            // handle fetching new token
        }
        return response.json();
    }

    async postFetch(url, body){
        return await pRetry(() => this.postRun(url, body), {retries: 0})
    }

    async getFetch(url){
        return await pRetry(() => this.getRun(url), {retries: 0})
    }
}

export default new HttpService();