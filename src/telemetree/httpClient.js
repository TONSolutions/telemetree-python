const axios = require('axios');

class HttpClient {
    constructor(settings) {
        this.settings = settings;
        this.url = this.settings.config.host;
        this.apiKey = this.settings.apiKey;
        this.projectId = this.settings.projectId;
    }

    async post(data) {
        try {
            const headers = {
                'Content-Type': 'application/json',
                'x-api-key': this.apiKey,
                'x-project-id': this.projectId
            };

            const response = await axios.post(this.url, data, { headers });

            return response;
        } catch (error) {
            console.error("Failed to send POST request:", error);
            throw error;
        }
    }
}

module.exports = { HttpClient };
