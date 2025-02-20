import telebot
from  config import TOKEN, keys
from extensions import APIException, get_price


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу, отправте сообщение боту в виде <имя валюты, \
цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>, для получения списка доступных валют введите команду /values"
    bot.reply_to(message, text)

@bot.message_handler(commands = ["values"])
def values(message: telebot.types.Message):
    text = "валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное колличество параметров')
        quote, base, amount = values
        meaning = get_price.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} - {meaning}'
        bot.send_message(message.chat.id, text)


bot.polling()