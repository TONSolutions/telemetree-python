const axios = require('axios');

class Config {
    constructor(apiKey, projectId) {
        this.apiKey = apiKey;
        this.projectId = projectId;
        this.config = this.fetchConfig();
    }

    async fetchConfig() {
        try {
            const response = await axios.get(`https://config.ton.solutions/v1/client/config?project=${this.projectId}`, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`
                }
            });

            if (response.status !== 200) {
                throw new Error(`Failed to fetch the config. Status code: ${response.status}`);
            }

            const config = response.data;

            const transformationDictionary = {
                "ChosenInlineQueryResult": "chosen_inline_result",
                "InlineQueryCalled": "inline_query",
                "PreCheckoutQuery": "pre_checkout_query"
            };

            config.auto_capture_telegram_events = config.auto_capture_telegram_events.map(event => {
                return transformationDictionary[event] || event;
            });

            config.auto_capture_commands = [...config.auto_capture_commands, ...config.auto_capture_messages];

            return config;
        } catch (error) {
            console.error("Error fetching config:", error);
            throw error;
        }
    }

    setApiKey(apiKey) {
        this.apiKey = apiKey;
    }

    setProjectId(projectId) {
        this.projectId = projectId;
    }

    getCredentials() {
        return {
            apiKey: this.apiKey,
            projectId: this.projectId
        };
    }
}

module.exports = { Config };
