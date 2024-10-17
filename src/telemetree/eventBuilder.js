const { Update } = require('./telegramSchemas');
const { Config } = require('./config');

class EventBuilder {
    constructor(settings) {
        this.settings = settings;
        this.config = this.settings.config;
        this.eventsToTrack = new Set(this.config.auto_capture_telegram_events);
        this.commandsToTrack = new Set(this.config.auto_capture_commands);
        this.appName = this.config.app_name;
    }

    parseTelegramUpdate(updateDict) {
        const update = new Update(updateDict);
        update.app_name = this.appName;

        return this.shouldTrackUpdate(update) ? update : null;
    }

    shouldTrackUpdate(update) {
        if (this.isTrackableMessageEvent(update)) {
            return this.shouldTrackMessage(update);
        }
        return this.shouldTrackEvent(update);
    }

    isTrackableMessageEvent(update) {
        return this.eventsToTrack.has('message') && (update.message || update.edited_message);
    }

    shouldTrackMessage(update) {
        const messageText = update.message ? update.message.text : update.edited_message.text;
        return Array.from(this.commandsToTrack).some(command => messageText.includes(command));
    }

    shouldTrackEvent(update) {
        return Array.from(this.eventsToTrack).some(event => update[event] !== undefined);
    }
}

module.exports = { EventBuilder };
