import telebot
bot = telebot.TeleBot('1188152490:AAHPNoGWYR7LY8b_0aqcNuKov9TCXar_Tk0')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

bot.polling()
