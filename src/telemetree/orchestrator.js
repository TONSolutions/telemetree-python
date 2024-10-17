const { resolveInlineMessageId, getPeer } = require('telethon.utils');
const { PeerUser, PeerChat, PeerChannel } = require('telethon.tl.types');
const telethon = require('telethon');

class ForwardedEventHandler {
    constructor() {
        this.payload = {};
    }

    sanitizeData(data) {
        if (typeof data === 'object') {
            if (Array.isArray(data)) {
                return data.map(this.sanitizeData);
            } else {
                return Object.keys(data).reduce((acc, key) => {
                    acc[key] = this.sanitizeData(data[key]);
                    return acc;
                }, {});
            }
        } else if (typeof data === 'string') {
            return data.replace(/[^a-zA-Z0-9_ .,@!-]/g, '');
        } else {
            return data;
        }
    }

    validateData(data) {
        const essentialKeys = ['context', 'body'];
        const missingKeys = essentialKeys.filter(key => !data.hasOwnProperty(key));
        if (missingKeys.length > 0) {
            throw new Error(`Missing essential data keys: ${missingKeys.join(', ')}`);
        }
    }

    handleInlineMessage(inlineMessageId) {
        try {
            const [messageId, peer, dcId, accessHash] = resolveInlineMessageId(inlineMessageId);
            return { messageId, peer, dcId, accessHash };
        } catch (error) {
            if (error instanceof telethon.errors.rpcerrorlist.MessageIdInvalidError) {
                return null;
            }
            throw error;
        }
    }

    eventHandlerMapping() {
        return {
            'chosen_inline_result': this.handleChosenInlineResult.bind(this),
            'inline_query': this.handleInlineQuery.bind(this),
            'my_chat_member': this.handleChatMemberUpdate.bind(this),
            'message': this.handleMessage.bind(this),
        };
    }

    orchestrator(update) {
        this.collectRequestContextData();
        const eventType = Object.keys(this.eventHandlerMapping()).find(key => update[key] !== undefined);

        this.payload.app = update.appName || 'bot';
        this.payload.eventSource = 'node-sdk-v2';
        this.payload.isAutocapture = true;
        this.payload.eventType = eventType ? eventType.replace('/', '') : null;

        if (eventType) {
            this.eventHandlerMapping()[eventType](update);
        }

        this.payload.eventparams = this.payload.eventDetails?.params || {};
        this.payload.eventdetails = {
            startParameter: this.payload.eventDetails?.startParameter || 'N/A',
            path: this.payload.eventDetails?.path || 'N/A',
        };

        this.payload.referrerType = this.payload.referrerType || 'Direct';
        this.payload.referrer = this.payload.referrer || '0';
        this.payload.sessionIdentifier = this.payload.sessionIdentifier;

        return this.payload;
    }

    collectRequestContextData() {
        this.payload.timestamp = Math.floor(Date.now() / 1000);
    }

    collectFromInfo(fromObject) {
        const userId = fromObject.entity_id || fromObject.id;
        this.payload.telegramID = String(userId);
        this.payload.isBot = fromObject.is_bot || false;
        this.payload.language = fromObject.language_code || 'N/A';
        this.payload.device = 'unknown';

        this.payload.userDetails = {
            username: fromObject.username || '',
            firstName: fromObject.first_name || '',
            lastName: fromObject.last_name || '',
            isPremium: fromObject.is_premium || false,
            writeAccess: true,
        };
    }

    handleInlineQuery(body) {
        const inlineQuery = body.inline_query;
        this.payload.eventType = 'Inline query';
        this.payload.eventDetails = {
            startParameter: inlineQuery.query,
            path: '',
        };
        this.collectFromInfo(inlineQuery.from);
    }

    handleChosenInlineResult(body) {
        const chosenInlineResult = body.chosen_inline_result;
        this.payload.eventType = 'Chosen inline query';
        this.payload.eventDetails = {
            startParameter: chosenInlineResult.query,
            result: chosenInlineResult.result_id,
            path: '',
        };
        const inlineMessageId = this.handleInlineMessage(chosenInlineResult.inline_message_id);
        if (inlineMessageId) {
            const resolvedPeer = getPeer(inlineMessageId.peer);
            this.assignChatTypeDetails(resolvedPeer, inlineMessageId);
        }
        this.collectFromInfo(chosenInlineResult.from);
    }

    handleChatMemberUpdate(body) {
        const myChatMember = body.my_chat_member;
        this.payload.eventType = 'Chat member update';

        const chatDetails = {
            chatType: myChatMember.chat.type,
            chatId: myChatMember.chat.id,
        };

        const oldStatus = myChatMember.old_chat_member.status;
        const newStatus = myChatMember.new_chat_member.status;

        let updateType;
        if (oldStatus !== newStatus) {
            switch (newStatus) {
                case 'member':
                    updateType = 'User joined';
                    break;
                case 'left':
                    updateType = 'User left';
                    break;
                case 'kicked':
                    updateType = 'User kicked/banned';
                    break;
                case 'administrator':
                    updateType = 'User promoted to administrator';
                    break;
                case 'restricted':
                    updateType = 'User restricted';
                    break;
                default:
                    updateType = 'Other';
            }
        } else {
            updateType = 'No change';
        }

        this.payload.eventDetails = {
            ...chatDetails,
            path: '',
            startParameter: '',
            updateType,
            oldStatus,
            newStatus,
        };

        this.collectFromInfo(myChatMember.from);
    }

    handleMessage(body) {
        const message = body.message;
        this.payload.eventType = 'Message';

        const chatId = message.chat.id || message.from.entity_id;

        this.payload.eventDetails = {
            startParameter: message.text || '',
            path: '',
            chatType: message.chat.type,
            chatId,
            messageId: message.message_id,
            text: message.text || '',
            messageLength: (message.text || '').length,
        };

        if (message.text && message.text.includes('/start')) {
            const parts = message.text.split(' ');
            this.payload.eventDetails.startParameter = parts.length > 1 ? parts[1] : '';
        }

        this.collectFromInfo(message.chat);
    }

    assignChatTypeDetails(resolvedPeer, inlineMessageId) {
        const eventDetails = this.payload.eventDetails || {};
        if (resolvedPeer instanceof PeerUser) {
            eventDetails.chatType = 'private';
            eventDetails.chat = resolvedPeer.user_id;
        } else if (resolvedPeer instanceof PeerChannel) {
            eventDetails.chatType = 'channel';
            eventDetails.chat = `https://t.me/c/${resolvedPeer.channel_id}/${inlineMessageId.messageId}`;
        } else if (resolvedPeer instanceof PeerChat) {
            eventDetails.chatType = 'chat';
            eventDetails.chat = `https://t.me/c/${resolvedPeer.chat_id}/${inlineMessageId.messageId}`;
        }
        this.payload.eventDetails = eventDetails;
    }
}

function orchestrateEvent(event) {
    const handler = new ForwardedEventHandler();
    return handler.orchestrator(event);
}

module.exports = { orchestrateEvent };
