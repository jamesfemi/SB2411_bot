import os
import telebot

# 1. Initialize Bot using the Token from Render's environment
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

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
    
    # Simple split for words
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

# 4. Start Long Polling (Infinite loop checking for messages)
if __name__ == "__main__":
    print("Bot is starting up...")
    # This keeps the bot running infinitely on your background worker
    bot.infinity_polling()
