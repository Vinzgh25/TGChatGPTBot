# Import necessary libraries
import telebot
import requests
import sqlite3
import shutil
import os

# Get Telegram bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
  raise RuntimeError("Specify TELEGRAM_BOT_TOKEN in the OS environment")

# Get OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
  raise RuntimeError("Specify OPENAI_API_KEY in the OS environment")

# Error message to display when something goes wrong
ERROR_MESSAGE = "Oops, something went wrong! Please try again later."

# URL for OpenAI API
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Headers to include in OpenAI API requests
OPENAI_API_HEADERS = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

# Create a Telegram bot object using the provided token
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# Handler for /start command
@bot.message_handler(commands=["start"])
def handle_start(message):
  # Connect to a SQLite database for this chat's history
  conn = sqlite3.connect(f"db/{message.chat.id}.sqlite3")

  # Create a cursor to execute SQL queries
  cur = conn.cursor()

  # Create a table to store conversation history if it doesn't already exist
  cur.execute("CREATE TABLE IF NOT EXISTS conversation (message TEXT)")

  # Commit the changes to the database
  conn.commit()


# Handler for /exit and /clear commands
@bot.message_handler(commands=["exit", "clear"])
def handle_exit(message):
  # Construct the path to the user's database file
  db_path = f"db/{message.chat.id}.sqlite3"

  # Check if the database file exists
  if os.path.exists(db_path):
    # If it does, delete the file
    os.remove(db_path)


# Default handler for all other messages
@bot.message_handler()
def handle_message(message):
  # Connect to this chat's SQLite database
  conn = sqlite3.connect(f"db/{message.chat.id}.sqlite3")

  # Create a cursor to execute SQL queries
  cur = conn.cursor()

  # Create a table to store conversation history if it doesn't already exist
  cur.execute("CREATE TABLE IF NOT EXISTS conversation (message TEXT)")

  # Retrieve all previous messages from the conversation table
  cur.execute("SELECT message FROM conversation")

  # Retrieve all messages from the conversation table
  conversation_messages = cur.fetchall()

  # Create a list of messages with their roles and content
  messages = []
  for i, content in enumerate(conversation_messages):
    messages.append({
      "role": "assistant" if i % 2 else "user",
      "content": content[0]
    })

  # Add the current message as a new user message to the list
  messages.append({"role": "user", "content": message.text})

  # Create a JSON payload to send to the OpenAI API
  json_payload = {"model": "gpt-3.5-turbo", "messages": messages}

  # Send a POST request to the OpenAI API with the JSON payload and headers
  response = requests.post(url=OPENAI_API_URL,
                           headers=OPENAI_API_HEADERS,
                           json=json_payload)

  # If the response is not OK, reply with the error message and return
  if not response.ok:
    bot.reply_to(message, ERROR_MESSAGE)
    return

  # Parse the JSON response and extract the first answer
  response_json = response.json()
  answer = response_json["choices"][0]["message"]["content"]

  # Reply to the user with the answer
  bot.reply_to(message, answer)

  # Create a new cursor to execute SQL queries
  cur = conn.cursor()

  # Insert the user's message and the AI's answer into the conversation table
  cur.executemany("INSERT INTO conversation (message) VALUES (?)",
                  ((message.text, ), (answer, )))

  # Commit the changes to the database
  conn.commit()


# Main function to run the bot
def main():
  # Delete existing "db" directory and its contents
  if os.path.isdir("db"):
    shutil.rmtree("db")

  # Create a new "db" directory
  os.mkdir("db")

  # Start polling for new messages from the Telegram bot
  bot.polling()


# This block is the entry point of the script.
if __name__ == "__main__":
  main()
