import telebot
from config import keys, TOKEN
from extensions import ConvertionException, MoneyConverter
bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     f"{message.chat.username}, добро пожаловать в бот Money Converter!\nДанный бот умеет конвертировать валюты.\n\nВведите команду /values для отображения поддерживаемых на данный момент валют.\n\nВведите запрос для расчета конвертации валюты в формате\n[Название конвертируемой валюты] [Название валюты, в которую конвертируем] [Сумма]\n\nПример:\nдоллар рубль 150")


# Обрабатываются все сообщения содержащие команды '/values'.
@bot.message_handler(commands=['values'])
def values(message):
    valuesAnswer = "Доступные валюты для конвертаций:"
    for key in keys.keys():
        valuesAnswer = '\n'.join((valuesAnswer, key,))
    bot.reply_to(message, valuesAnswer)


# Обработка текстового запроса
@bot.message_handler(content_types=['text', ])
def convertMoney(message):
    try:
        values = message.text.split(' ')
        if (len(values) != 3):
            raise ConvertionException(f'Не верное кол-во параметров в запросе.\nПереданное кол-во параметров: {len(values)}')

        moneyIn, moneyOut, amount = message.text.split(' ')
        moneyResult = round(MoneyConverter.get_price(moneyIn, moneyOut, amount), 2)
    except ConvertionException as e:
        bot.reply_to(message, f'Возникла ошибка на стороне пользователя при вводе данных:\n{e}\n\nИспользуйте команду /help для получения справки по работе с ботом.')
    except Exception as e:
        bot.reply_to(message, f'При обработке запроса возникла ошибка:\n{e}\n\nИспользуйте команду /help для получения справки по работе с ботом.')
    else:
        answer = f'{float(amount):,.2f} {moneyIn} = {moneyResult:,.2f} {moneyOut}'
        bot.reply_to(message, answer)

bot.polling(none_stop=True)
