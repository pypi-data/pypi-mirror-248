"""Declare all global constants."""

COMMANDS = {
    "start": "Restart bot",
    "id": "Get details ID of a message",
    "get": "Forward any posts from public channel",
    "help": "Learn usage",
    "report": "Send a message to the bot Admin",
}

REGISTER_COMMANDS = True

KEEP_LAST_MANY = 10000

CONFIG_FILE_NAME = "tgcf.config.json"
CONFIG_ENV_VAR_NAME = "TGCF_CONFIG"

MONGO_DB_NAME = "tgcf-config"
MONGO_COL_NAME = "tgcf-instance-0"

BOT_CONFIG_FILE_NAME = "bot.config.json"
BOT_CONFIG_ENV_VAR_NAME = "TGCF_BOT_CONFIG"