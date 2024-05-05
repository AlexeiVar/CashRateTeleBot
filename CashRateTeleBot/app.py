from config import TOKEN
import extensions
import telebot

bot = telebot.TeleBot(TOKEN)
converter = extensions.Converter


@bot.message_handler(commands=['start', 'help'])
def info(message: telebot.types.Message):
    text = ("Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> <в какую "
            "валюту перевести> <сумма переводимой валюты>\n Чтобы узнать какие валюты доступны введите команду /values")
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты для бота:"
    for key in extensions.currency_list:
        text += f'\n {extensions.currency_list[key]} - {key}'
    bot.send_message(message.chat.id, text)


@bot.message_handler()
def convert(message: telebot.types.Message):
    try:
        text = converter.exchange(message)
    except extensions.APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать комманду\n {e}")
    else:
        bot.send_message(message.chat.id, text)


bot.polling()
