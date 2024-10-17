![](https://tc-images-api.s3.eu-central-1.amazonaws.com/gif_cropped.gif)
# Telemetree Node.js SDK
[![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.org/project/pip/)
[![PyPI pyversions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)](https://test.pypi.org/project/telemetree/0.1.1/)

The Telemetree Node.js SDK provides a convenient way to track and analyze Telegram events using the Telemetree service. With this SDK, you can easily capture and send Telegram events to the Telemetree platform for further analysis and insights.

![Alt](https://repobeats.axiom.co/api/embed/18ee5bb9c80b65e0e060cd5b16802b38262b2a87.svg "Repobeats analytics image")

### Features

- Automatically capture Telegram events and send them to Telemetree
- Encrypt event data using a hybrid approach with RSA and AES encryption
- Customize the events and commands to track
- Simple and intuitive API for easy integration

### Installation

You can install the Telemetree Node.js SDK using npm:

```shell
npm install telemetree
```

### Usage

1. Import the Telemetree SDK:

```javascript
const { TelemetreeClient } = require('telemetree');
```

2. Initialize the client with your API key and project ID:

```javascript
const apiKey = "YOUR_API_KEY";
const projectId = "YOUR_PROJECT_ID";

const client = new TelemetreeClient(apiKey, projectId);
```

3. Connect the client to your webhook, or pass the event data directly:

```javascript
const event = {
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

const responseStatusCode = client.track(event);
console.log(responseStatusCode);
```

### Configuration

The Telemetree Node.js SDK provides some configuration options that you can customize:

- `auto_capture_telegram`: Enables or disables automatic capturing of Telegram events (default: `True`)
- `auto_capture_telegram_events`: Specifies the types of Telegram events to capture automatically (default: `["message"]`)
- `auto_capture_commands`: Specifies the Telegram commands to capture automatically (default: `["/start", "/help"]`)

Other configuration options include the Telemetree API endpoint, encryption keys, and logging settings. You can modify these options either within the Telemetree dashboard or by updating the `config.js` file in the SDK.

### Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

### License

This project is licensed under the MIT License. See the LICENSE file for more information.

### Support

If you have any questions or need assistance, please contact our support team at support@ton.solutions.
