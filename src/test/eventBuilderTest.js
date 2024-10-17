const { expect } = require('chai');
const { EventBuilder } = require('../telemetree/eventBuilder');
const { Config } = require('../telemetree/config');

describe('EventBuilder', () => {
    let eventBuilder;

    before(async () => {
        const config = new Config('dummy_api_key', 'dummy_project_id');
        await config.fetchConfig();
        eventBuilder = new EventBuilder(config);
    });

    describe('parseTelegramUpdate', () => {
        it('should parse a valid message update', () => {
            const update = {
                update_id: 123456789,
                message: {
                    message_id: 1,
                    from: {
                        id: 987654321,
                        is_bot: false,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        language_code: "en"
                    },
                    chat: {
                        id: 987654321,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        type: "private"
                    },
                    date: 1621234567,
                    text: "Hello, world!"
                }
            };

            const result = eventBuilder.parseTelegramUpdate(update);
            expect(result).to.not.be.null;
        });

        it('should return null for an invalid message update', () => {
            const update = {
                update_id: 123456789,
                message: {
                    message_id: 1,
                    from: {
                        id: 987654321,
                        is_bot: false,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        language_code: "en"
                    },
                    chat: {
                        id: 987654321,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        type: "private"
                    },
                    date: 1621234567,
                    text: "Invalid message"
                }
            };

            const result = eventBuilder.parseTelegramUpdate(update);
            expect(result).to.be.null;
        });

        it('should parse a valid edited message update', () => {
            const update = {
                update_id: 123456789,
                edited_message: {
                    message_id: 1,
                    from: {
                        id: 987654321,
                        is_bot: false,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        language_code: "en"
                    },
                    chat: {
                        id: 987654321,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        type: "private"
                    },
                    date: 1621234567,
                    edit_date: 1621234570,
                    text: "Edited message"
                }
            };

            const result = eventBuilder.parseTelegramUpdate(update);
            expect(result).to.not.be.null;
        });

        it('should return null for an invalid edited message update', () => {
            const update = {
                update_id: 123456789,
                edited_message: {
                    message_id: 1,
                    from: {
                        id: 987654321,
                        is_bot: false,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        language_code: "en"
                    },
                    chat: {
                        id: 987654321,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        type: "private"
                    },
                    date: 1621234567,
                    edit_date: 1621234570,
                    text: "Invalid edited message"
                }
            };

            const result = eventBuilder.parseTelegramUpdate(update);
            expect(result).to.be.null;
        });

        it('should parse a valid inline query update', () => {
            const update = {
                update_id: 123456789,
                inline_query: {
                    id: "123456789",
                    from: {
                        id: 987654321,
                        is_bot: false,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        language_code: "en"
                    },
                    query: "test query",
                    offset: ""
                }
            };

            const result = eventBuilder.parseTelegramUpdate(update);
            expect(result).to.not.be.null;
        });

        it('should parse a valid chosen inline result update', () => {
            const update = {
                update_id: 123456789,
                chosen_inline_result: {
                    from: {
                        id: 987654321,
                        is_bot: false,
                        first_name: "John",
                        last_name: "Doe",
                        username: "johndoe",
                        language_code: "en"
                    },
                    inline_message_id: "123456789",
                    query: "test query",
                    result_id: "result_1"
                }
            };

            const result = eventBuilder.parseTelegramUpdate(update);
            expect(result).to.not.be.null;
        });
    });
});
