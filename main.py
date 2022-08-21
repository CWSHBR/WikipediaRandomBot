import telebot, wikipedia
from random import randint
import os
from telebot import types
from keyboa import Keyboa


wikipedia.set_lang("ru")
bot = telebot.TeleBot("5526826010:AAHHa4FraTMsGXBaoCVXgDSI2lJwClTIsYc")

cwd, file = os.path.split(__file__)

wordDict = cwd + "\\dict.txt"

with open(wordDict) as f:
    lines = f.readlines()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'b>Привіт, це чат бот вікіпедії, щоб дізнатися інформацію про цього бота натисни на "/help",'
                     ' щоб дізнатися якусь статтю натисни на "/page", щоб звязатися з розробником натисни "/info"</b>', parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,
                     '<b>Цей бот видасть тобі випадкову статтю з Wikipedia, Просто напиши "/page"</b>',
                     parse_mode='html')


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, '<b>телеграм розробника: @lar1us2, пропонуйте ідеї що додати в бота)</b>', parse_mode='html')


def wikiRandomSearch():
    while True: #solving empty range bug
        word = lines[randint(0, len(lines) - 1)]
        print("-> Word: " + word)
        wiki = wikipedia.search(word)
        print("-> Wiki search index: " + str(len(wiki)) +"\n")
        if(len(wiki) > 0):
            break
        else:
            print("! Not found in Wikipedia. Trying again...\n")
    return wiki

@bot.message_handler(commands=['page'])
def page(message):
    print("--------- Random article searching started --------")
    print("@ Name: "+ message.from_user.first_name + "\n@ Username: "+ message.from_user.username+"\n")

    mess = bot.send_message(message.chat.id, "Пожалуйста, подождите...", parse_mode='html')
    
    article = ""

    while True: #solving DisambiguationError
        try:
            wiki = wikiRandomSearch()
            article = wikipedia.page(wiki[randint(0, len(wiki) - 1)])
            break
        except Exception as e:
            print("! Error: " + str(e) + " \nBut don't worry. We try to do it again!\n")
            continue

    print("✓ Article: " + article.title)
    buttons = []
    buttons.append({"text":"Продолжить чтение ->", "url":article.url})
    keyboard = Keyboa(items=buttons).keyboard
    #bot.send_message(message.chat.id, f'<b>{article.title}</b>\n\n{article.summary[:400]}...',parse_mode='html', reply_markup= keyboard)
    bot.edit_message_text(text= f'<b>{article.title}</b>\n\n{article.summary[:400]}...', chat_id=mess.chat.id, message_id=mess.message_id, parse_mode='html', reply_markup= keyboard)
    print("--------- Random article searching ended --------\n")

bot.polling(none_stop = True)