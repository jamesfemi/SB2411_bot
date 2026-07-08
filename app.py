import os
from flask import Flask, request
import telebot

# 1. Initialize Bot and Flask Web Server
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 2. Start Command (/start) in Khmer
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "សួស្តី! ខ្ញុំជាប៊ុតរាប់តួអក្សរ។ 🇰🇭\n\n"
        "សូមផ្ញើអត្ថបទណាមួយមកខ្ញុំ ខ្ញុំនឹងប្រាប់អ្នកអំពី៖\n"
        "• ចំនួនតួអក្សរសរុប\n"
        "• ចំនួនតួអក្សរ (មិនគិតដកឃ្លា)\n"
        "• ចំនួនពាក្យ\n"
        "• ចំនួនកថាខណ្ឌ"
    )
    bot.reply_to(message, welcome_text)

# 3. Text Counter Logic
@bot.message_handler(func=lambda message: True)
def count_text(message):
    text = message.text
    
    total_chars = len(text)
    chars_no_spaces = len(text.replace(" ", "").replace("\n", ""))
    
    # Simple split for words (Note: Khmer text without spaces requires advanced NLP segmentation, 
    # but this handles standard spaces/mix text gracefully)
    words = len(text.split()) if text.strip() else 0
    paragraphs = len([p for p in text.split('\n') if p.strip()])
    
    reply_text = (
        f"📊 **លទ្ធផលនៃការរាប់អត្ថបទរបស់អ្នក៖**\n\n"
        f"• តួអក្សរសរុប (រួមទាំងដកឃ្លា)៖ **{total_chars}**\n"
        f"• តួអក្សរ (មិនគិតដកឃ្លា)៖ **{chars_no_spaces}**\n"
        f"• ចំនួនពាក្យ៖ **{words}**\n"
        f"• ចំនួនកថាខណ្ឌ៖ **{paragraphs}**"
    )
    bot.reply_to(message, reply_text, parse_mode='Markdown')

# 4. Webhook setup so Render can route Telegram messages to our code
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # Replace URL later with your actual Render URL
    RENDER_URL = os.environ.get('RENDER_EXTERNAL_URL')
    if RENDER_URL:
        bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
        return "Webhook Set Successfully!", 200
    return "Bot is running, but RENDER_EXTERNAL_URL environment variable is missing.", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
