# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from flask import Flask, request
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
import telegram
import valve.source.a2s 

app = Flask(__name__)
app.debug = True

TOKEN = "344036403:AAE9H0YR9_bTlw5uQm6PUzKG97ziq4GUdBQ"

global bot 
bot = telegram.Bot(token=TOKEN)

URL = '95.85.39.36' 

server_address = (URL, 27015)
server = valve.source.a2s.ServerQuerier(server_address)

#WebHook
@app.route('/HOOK', methods=['POST', 'GET']) 
def webhook_handler():
    if request.method == "POST": 
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        try:
            kb = ReplyKeyboardMarkup([["Обновить"]])
            chat_id = update.message.chat.id 
            text = update.message.text
            userid = update.message.from_user.id
            username = update.message.from_user.username
            bot.send_message(chat_id=chat_id, text=get_info(), reply_markup=kb)
        except Exception, e:
            print e
    return 'ok' 

#Set_webhook 
@app.route('/set_webhook', methods=['GET', 'POST']) 
def set_webhook(): 
    s = bot.setWebhook('https://%s:443/HOOK' % URL, certificate=open('/etc/ssl/server.crt', 'rb')) 
    if s:
        print(s)
        return "webhook setup ok" 
    else: 
        return "webhook setup failed" 

@app.route('/') 
def index(): 
    return '<h1>Hello</h1>' 

def get_info():
    info = server.get_info()
    players = server.get_players()

    answer = "<b>Server name:</b> {server_name}\n<b>Game:</b> {game}\n<b>Players:</b> {player_count}/{max_players} \n".format(**info)
    for player in sorted(players["players"],
                         key=lambda p: p["score"], reverse=True):
        answer += "<b>{name}</b> {score} <i>Duration: {duration}</i>a\n".format(**player)

    return answer