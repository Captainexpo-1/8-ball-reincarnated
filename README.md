# 8-ball-reincarnated

This is a simple Slack bot that uses OpenAI's GPT-3 to answer questions.

## Installation

1. Clone the repository
2. Install the dependencies
3. Set up the `.env`
4. Run the bot

### Setting up the `.env`

Copy the `.env.example` file to `.env` and fill in the required values:

```env
OPENAI_API_KEY=your openai api key
SIGNING_SECRET=your slack signing secret
SLACK_TOKEN=the xoxb token of the bot
PORT=the port you want the bot to run on, usually 3000
ENV=development or production depending on your environment
STATUS_CHANNEL=The channel ID of the channel you want to send the status message to
```

## Usage

To use the bot, simply mention it in a channel and ask a question. For example:

```
You: @8-ball-reincarnated What is the meaning of life?

8-ball-reincarnated: The meaning of life is like a jar of pickles - salty, sour, and best enjoyed with friends. :cucumber:
```

