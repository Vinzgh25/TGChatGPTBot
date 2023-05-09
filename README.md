# TGChatGPTBot

TGChatGPTBot is a powerful and intuitive chatbot that uses the OpenAI API to provide natural language conversation support to Telegram users. Whether you need help with customer service inquiries, product recommendations, or just want to have a friendly chat, TGChatGPTBot is here to help!

## Features

- Intelligent natural language processing
- Personalized responses based on user input
- Multi-language support
- Integration with external APIs for extended functionality
- Quick and easy setup

## Getting Started

To start using TGChatGPTBot, simply add it to your Telegram contacts and start chatting! The bot will automatically detect your language and provide personalized responses to your messages.

## Running

Run the following commands to start TGChatGPTBot.

1. Clone the repository to your local machine.

```bash
git clone https://github.com/TheNekJT/TGChatGPTBot.git && cd TGChatGPTBot
```

2. Install the required dependencies listed in `pyproject.toml`. You can use pip to install them automatically by running:

```bash
pip install -e .
```

3. Create a .env file in the root directory of the project and add your Telegram bot token and OpenAI API key to it as `TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY` environment variables, respectively. For example:

```bash
export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

4. Run the `main.py` script in your terminal to start the bot. For example:

```bash
python main.py
```

5. Once the bot is running, open Telegram and start a conversation with it to test its functionality.

## Contributing

If you would like to contribute to TGChatGPTBot, please fork the repository and submit a pull request. We are always looking for ways to improve the bot and welcome any feedback or suggestions.

## Credits

TGChatGPTBot is developed and maintained by [TheNekJT](https://github.com/TheNekJT). Special thanks to the OpenAI team for their incredible API and support.
