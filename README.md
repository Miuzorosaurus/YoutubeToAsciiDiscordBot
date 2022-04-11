# YoutubeToAsciiDiscordBot
A discord bot that downloads and processes a YouTube video, and turns it into ascii art in messages.

Requires an token.env file in the same directory, which contains:

TOKEN=your_discord_bot_token

The font file is used by imagemaker.py

Supports both ascii text and ascii image output

Supports playing in multiple channels, however due to rate limit it's not recommended.

Running videomaker.py as standalone is also supported, and takes command line arguments.
