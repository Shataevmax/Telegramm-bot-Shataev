import telebot
from extensions import *
from config import *

bot = telebot.TeleBot(TOKEN)


'''@bot.message_handler()
def echo_test(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'hello')'''

@bot.message_handler(commands=['start', 'help'])
def help (message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\
\n увидеть список всех доступных валют /values   '
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = value
        total_base = CryptoConvecter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать командку\n{e}')
    else:
        text = f'цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling( )
