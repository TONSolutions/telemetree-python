![](https://tc-images-api.s3.eu-central-1.amazonaws.com/gif_cropped.gif)
# Telemetree Python SDK
[![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.org/project/pip/)
[![PyPI pyversions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)](https://test.pypi.org/project/telemetree/0.1.1/)

The Telemetree Python SDK provides a convenient way to track and analyze Telegram events using the Telemetree service. With this SDK, you can easily capture and send Telegram events to the Telemetree platform for further analysis and insights.

### Features

- Automatically capture Telegram events and send them to Telemetree
- Encrypt event data using a hybrid approach with RSA and AES encryption
- Customize the events and commands to track
- Simple and intuitive API for easy integration

### Installation

You can install the Telemetree Python SDK using pip:

```shell
pip install telemetree
```

### Usage

1. Import the Telemetree SDK:

```python
from telemetree import TelemetreeClient
```

2. Initialize the client with your API key and project ID:

```python
api_key = "YOUR_API_KEY"
project_id = "YOUR_PROJECT_ID"

client = TelemetreeClient(api_key, project_id)
```

3. Connect the client to your webhook, or pass the event data directly:

```python
event = {
    "update_id": 123456789,
    "message": {
        "message_id": 1,
        "from": {
            "id": 987654321,
            "is_bot": False,
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "language_code": "en"
        },
        "chat": {
            "id": 987654321,
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "type": "private"
        },
        "date": 1621234567,
        "text": "Hello, world!"
    }
}

response_status_code = client.track(event)
print(response_status_code)
```

### Configuration

The Telemetree Python SDK provides some configuration options that you can customize:

- `auto_capture_telegram`: Enables or disables automatic capturing of Telegram events (default: `True`)
- `auto_capture_telegram_events`: Specifies the types of Telegram events to capture automatically (default: `["message"]`)
- `auto_capture_commands`: Specifies the Telegram commands to capture automatically (default: `["/start", "/help"]`)

Other configuration options include the Telemetree API endpoint, encryption keys, and logging settings. You can modify these options either within the Telemetree dashboard or by updating the `config.py` file in the SDK.

### Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

### License

This project is licensed under the MIT License. See the LICENSE file for more information.

### Support

If you have any questions or need assistance, please contact our support team at support@ton.solutions.
