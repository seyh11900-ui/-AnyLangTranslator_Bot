import os
import telebot
from deep_translator import GoogleTranslator

# Get token from environment variables (securely set in Railway)
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN environment variable found!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "🤖 *Language Translation Bot*\n\n"
        "Use the command below to translate text:\n"
        "`/translate <lang_code> <your text>`\n\n"
        "*Examples:*\n"
        "• `/translate es Hello, how are you?` (Spanish)\n"
        "• `/translate fr Good morning` (French)\n"
        "• `/translate ja Thank you` (Japanese)\n\n"
        "*Common Language Codes:*\n"
        "`en` (English) | `es` (Spanish) | `fr` (French) | `de` (German) | "
        "`ja` (Japanese) | `zh` (Chinese) | `ru` (Russian) | `ar` (Arabic)"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['translate'])
def translate_text(message):
    try:
        # Expected format: /translate <lang> <text>
        parts = message.text.split(' ', 2)
        if len(parts) < 3:
            bot.reply_to(
                message, 
                "⚠️ Please provide a target language code and text.\n"
                "Example: `/translate es Hello world`", 
                parse_mode="Markdown"
            )
            return

        target_lang = parts[1].lower()
        text_to_translate = parts[2]

        # Perform auto-detection and translation
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text_to_translate)

        response = (
            f"🌐 *Translated to ({target_lang}):*\n"
            f"{translated}"
        )
        bot.reply_to(message, response, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, "❌ Translation failed. Make sure your language code is valid (e.g., `es`, `fr`, `de`).")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
