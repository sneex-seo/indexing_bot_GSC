import telebot
from telebot import types
from requests import *
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import time

JSON_KEY_FILE = "client_secrets.json"
Scopes = ["https://www.googleapis.com/auth/indexing"]

client = telebot.TeleBot("")

@client.message_handler(commands=["start"])

def Google_indexing_api(message):

    menu_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_buttons.add(types.KeyboardButton("Индексируем"), types.KeyboardButton("Удаляем"))

    msg = client.send_message(message.chat.id, "Что будем делать с ссылками?",reply_markup = menu_buttons)
    client.register_next_step_handler(msg, user_answer)

def user_answer(message):
    if message.text == "Индексируем":
        msg = client.send_message(message.chat.id, "Жду список ссылок") 
        client.register_next_step_handler(msg, user_links_list_for_index)
    elif message.text == "Удаляем":
        msg = client.send_message(message.chat.id, "Жду список ссылок") 
        client.register_next_step_handler(msg, user_links_list_for_deleting)
    else:
        client.send_message(message.chat.id("Ты ничего не выбрал"))

def user_links_list_for_index(message):
    indexing_list = message.text.split()
    for link_for_index in indexing_list:
        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        client.send_message(message.chat.id, 'Пробую просканировать: ' + link_for_index)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=Scopes)
        http = credentials.authorize(httplib2.Http())
        content = {}
        content['url'] = "https://listing3d.com/"
        content['type'] = "URL_UPDATED"
        json_ctn = json.dumps(content) 
                
        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)

        result = json.loads(content.decode())

         # For debug purpose only
        if("error" in result):
            client.send_message(message.chat.id, 'Ошибка попробуй позже')

        else:
            client.send_message(message.chat.id, 'Проиндексировал ссылку: ' + link_for_index)

        time.sleep(10)

def user_links_list_for_deleting(message):
    indexing_list = message.text.split()
    for link_for_index in indexing_list:
        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        client.send_message(message.chat.id, 'Пробую удалить: ' + link_for_index)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=Scopes)
        http = credentials.authorize(httplib2.Http())
        content = {}
        content['url'] = "https://listing3d.com/"
        content['type'] = "URL_DELETED"
        json_ctn = json.dumps(content) 
                
        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)

        result = json.loads(content.decode())

        print(result)

         # For debug purpose only
        if("error" in result):
            client.send_message(message.chat.id, 'Ошибка попробуй позже')

        else:
            client.send_message(message.chat.id, 'Отправил на удаление ссылку: ' + link_for_index)

        time.sleep(10)

client.polling(none_stop = True, interval = 0)
