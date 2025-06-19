from telebot import TeleBot
import pickle

with open('model.plk','rb') as file:
    model = pickle.load(file)

Token ='7745844397:AAGHmJFqTtRhoWYgzCrt6dtKO0LIOMfObU8'
bot = TeleBot(token = Token)

@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id,"👋 Բարև, ուղարկիր ինձ նորություն ես կդասակարգեմ այն 🤖")

@bot.message_handler()
def speaking(message):
    bot.send_message(message.chat.id,model.predict([message.text]))


bot.polling()