const { Config } = require('./config');
const { HttpClient } = require('./httpClient');
const { EncryptionService } = require('./encryption');
const { EventBuilder } = require('./eventBuilder');
const { orchestrateEvent } = require('./orchestrator');
const { convertPublicKey } = require('./utils');

class TelemetreeClient {
    constructor(apiKey, projectId) {
        this.apiKey = apiKey;
        this.projectId = projectId;

        this.settings = new Config(this.apiKey, this.projectId);

        this.publicKey = convertPublicKey(this.settings.config.public_key);

        this.encryptionService = new EncryptionService(this.publicKey);
        this.httpClient = new HttpClient(this.settings);
        this.eventBuilder = new EventBuilder(this.settings);
    }

    track(event) {
        try {
            const orchestratedEvent = orchestrateEvent(event);
            const encryptedEvent = this.encryptionService.encrypt(JSON.stringify(orchestratedEvent));
            const response = this.httpClient.post(encryptedEvent);
            return response.statusCode;
        } catch (e) {
            console.error("Error tracking event:", e);
        }
        return null;
    }
}

module.exports = { TelemetreeClient };
