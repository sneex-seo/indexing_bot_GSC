from oauth2client.service_account import ServiceAccountCredentials
import time
import httplib2
import json
import telebot 
import json

bot_token = '5933979018:AAGJKQmQwCgICOon7Y6Sjj5PrGryTIPq4MQ'
bot = telebot.TeleBot(bot_token)

JSON_KEY_FILE = "client_secrets.json"
Scopes = ["https://www.googleapis.com/auth/indexing"]


@bot.message_handler(content_types=["text"])

def indexing_method(message):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=Scopes)
    http = credentials.authorize(httplib2.Http())

    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    
    indexing_list = message.text.split()

    bot.send_message(message.chat.id, 'Получил список ссылок: ' + message.text)
  
    for link_for_index in indexing_list:
        bot.send_message(message.chat.id, 'Пробую просканировать: ' + link_for_index)
        content = {}
        content['url'] = link_for_index
        content['type'] = "URL_UPDATED"
        json_ctn = json.dumps(content)    
        
        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)

        result = json.loads(content.decode())

        print(result)

         # For debug purpose only
        if("error" in result):
            print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"], result["error"]["message"]))
            bot.send_message(message.chat.id, 'Ошибка попробуй позже')

        else:
            print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
            print("urlNotificationMetadata.latestUpdate.url: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["url"]))
            print("urlNotificationMetadata.latestUpdate.type: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["type"]))
            print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))
            bot.send_message(message.chat.id, 'Проиндексировал ссылку: ' + link_for_index)

        time.sleep(10)





while True: 
    try:      
        if __name__ == '__main__':
            bot.polling(none_stop=True)
    except:
        time.sleep(5)