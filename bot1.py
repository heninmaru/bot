import telebot
import config
from telebot import types
import random

letter2 = gods_message()
bot = telebot.TeleBot(config.TOKEN)
# варианты слов для игры "угадай слово"
words_list = ('программирование', 'вирус', 'фильм', 'бумага',
              'библиотека', 'игра', 'медицина', 'болезнь', 'отпуск')
# выбираем случайное слово для игры "угадай слово"
chosen_word = random.choice(words_list)
# слово для игры "угадай слово" становится XXXX...
gamer_word = ['X'] * len(chosen_word)


@bot.message_handler(commands=['start'])
def welcome(message):
    # указываем папку откуда берем стикер
    sti = open('kartin/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    # создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    chosen1 = types.KeyboardButton("Как у тебя проходит день? ")
    chosen2 = types.KeyboardButton("Поиграем в игру Угадай слово ")
    chosen3 = types.KeyboardButton("Поиграем в игру Крестики нолики ")
    markup.add(chosen1, chosen2, chosen3)
    
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!"
                                      "\nЯ - <b>{1.first_name}</b>, бот версии 1.0 созданный"
                                      " для развлечений ".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def msg(message):
    print("--------------------------------------------------------------")
    print(message.from_user.last_name)
    print(message.from_user.first_name)
    print("--------------------------------------------------------------")
    file_name = str(message.from_user.last_name) \
                + str(message.from_user.first_name) + ".txt"
    print(file_name)
    f = open(file_name, 'w')
    f.write(message.text + ' ')
    f.close()
    f = open(file_name, 'r')
    if f.read() == 'Как у тебя проходит день? ':
        ## Создаем инлайновую клавиатуру
        markup = types.InlineKeyboardMarkup(row_width=2)
        chosen1 = types.InlineKeyboardButton("Хорошо",
                                             callback_data='good')
        chosen2 = types.InlineKeyboardButton("Плохо",
                                             callback_data='bad')
        markup.add(chosen1, chosen2)
        bot.send_message(message.chat.id, 'Отлично, а у самого как?',
                         reply_markup=markup)
    else:
        f = open(file_name, 'r')
        if f.read() == 'Привет ':
            bot.send_message(message.chat.id, 'Привет. Поздравляю с '
                                              'нахождением секретной команды))) Нажми одну '
                                              'из кнопок для развлечения')
        else:
            f = open(file_name, 'r')
            if f.read() == 'Поиграем в игру Крестики нолики ':
                markup = types.InlineKeyboardMarkup(row_width=2)
                chosen3 = types.InlineKeyboardButton("X", callback_data='X')
                chosen4 = types.InlineKeyboardButton("0", callback_data='0')
                markup.add(chosen3, chosen4)
                bot.send_message(message.chat.id, 'За кого играть будешь?',
                                 reply_markup=markup)
            else:
                f = open(file_name, 'r')
                if f.read() == 'Поиграем в игру Угадай слово ':
                    bot.send_message(message.chat.id, "Тогда напиши одну"
                                    " русскую букву или любой символ. Начнем. У вас 8 "
                                                      "попыток)")
                else:
                    if len(message.text) == 1 and (message.text != "X" or message.text != "0" ):
                        bot.send_message(message.chat.id, 'Игра будет...в следующем обновлении.'
                                                          'До встречи')
                    else:
                        bot.send_message(message.chat.id, 'У меня просто нет слов (((')

## ответы на нажатие кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_chat(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Значит сегодня хороший день ))')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Как у тебя проходит день?", reply_markup=None)
            
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывают и плохие дни. Завтра будет лучше((')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Как у тебя проходит день?", reply_markup=None)
            
            elif call.data == 'X':
                bot.send_message(call.message.chat.id, 'Хорошо. Первый ход за вами...в следующем обновлении))) ))')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Поиграем в игру Крестики нолики", reply_markup=None)
            
            elif call.data == '0':
                bot.send_message(call.message.chat.id, 'Хорошо. Второй ход за вами...в следующем обновлении))) ))')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Поиграем в игру Крестики нолики", reply_markup=None)
            
            # при ответе на вопрос бота
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="спс за ответ")
    
    except Exception as e:
        print(repr(e))

if __name__ == '__main__':
    bot.infinity_polling()
