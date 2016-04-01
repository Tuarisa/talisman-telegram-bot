#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib 
import sys
import os
import string
import time
import urllib2

sys.path.append(os.path.join(os.path.abspath('.'), 'venv/lib/python2.7/site-packages'))
sys.path.append(os.path.join(os.path.abspath('.'), 'modules'))

import telegram
from flask import Flask, request

app = Flask(__name__)

import threading
GENERAL_CONFIG_FILE = 'config.txt'
fp = open(GENERAL_CONFIG_FILE, 'r')
GENERAL_CONFIG = eval(fp.read())
fp.close()
PLUGIN_DIR = 'plugins'
COMMANDS = {}
COMMAND_HANDLERS = {}

global bot
bot = telegram.Bot(token=GENERAL_CONFIG['TOKEN'])

###############################################################################################
@app.route('/HOOK', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True))
        try:
            # Telegram understands UTF-8, so encode text for unicode compatibility
            text = update.message.text.encode('utf-8') + ' '
            command = parseCommand(text)
            text = text.decode('utf-8')
            call_command_handlers(command.decode('utf-8').lower(),update,(text.split(' ',1))[1])
        except:
            #reply(update,'something wrong')
            return 'not ok'

    return 'ok'

@app.route('/debug/<message>', methods=['GET'])
def debug_handler(message):
    if request.method == "GET":
        text = message.encode('utf-8').decode('utf-8') + ' '
        command = parseCommand(text)
        call_command_handlers(command,DebugObj.returnFakeUpdate(),(text.split(' ',1))[1])
        return DebugObj.answer()


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook(GENERAL_CONFIG['URL']+'/HOOK')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return 'Hello'
###############################################################################################

def find_plugins():
    print '\nLOADING PLUGINS'
    valid_plugins = []
    invalid_plugins = []
    possibilities = os.listdir('plugins')
    for possibility in possibilities:
        if possibility[-3:].lower() == '.py':
            try:
                fp = file(PLUGIN_DIR + '/' + possibility)
                data = fp.read(23)
                if data == '#===istalismanplugin===':
                    valid_plugins.append(possibility)
                else:
                    invalid_plugins.append(possibility)
            except:
                pass
    if invalid_plugins:
        print '\nfailed to load',len(invalid_plugins),'plug-ins:'
        invalid_plugins.sort()
        invp=', '.join(invalid_plugins)
        print invp
        print 'plugins header is not corresponding\n'
    else:
        print '\nthere are not unloadable plug-ins'
    return valid_plugins

def load_plugins():
    plugins = find_plugins()
    for plugin in plugins:
        try:
            fp = file(PLUGIN_DIR + '/' + plugin)
            exec fp in globals()
            fp.close()
        except:
            raise
    plugins.sort()
    print '\nloaded',len(plugins),'plug-ins:'
    loaded=', '.join(plugins)
    print loaded,'\n'

def reply(source,text):
    chat_id = source.message.chat.id
    if (chat_id=='dbg'):
        DebugObj.sendMessage(chat_id, text)
        return
    bot.sendMessage(chat_id=chat_id,text=text)

def msg(chat_id, text):
    if (chat_id=='dbg'):
        DebugObj.sendMessage(chat_id, text)
        return
    bot.sendMessage(chat_id=chat_id,text=text)

def parseCommand(text):
    command = (text.split(' '))[0]
    if command[0]=='/':
        command = command[1:]
    return command

def register_command_handler(instance, command, category=[], access=0, desc='', syntax='', examples=[]):
    command = command.decode('utf-8')
    COMMAND_HANDLERS[command] = instance
    COMMANDS[command] = {'category': category, 'access': access, 'desc': desc, 'syntax': syntax, 'examples': examples}

def call_command_handlers(command, source, parameters):
    if COMMAND_HANDLERS.has_key(command):
        thred = threading.Thread(target = COMMAND_HANDLERS[command],args = (source,parameters))
        thred.start()
        thred.join()


def timeElapsed(time):
    minutes, seconds = divmod(time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30)
    rep = u'%d сек' % (round(seconds))
    if time>=60: rep = u'%d мин %s' % (minutes, rep)
    if time>=3600: rep = u'%d час %s' % (hours, rep)
    if time>=86400: rep = u'%d дн %s' % (days, rep)
    if time>=2592000: rep = u'%d мес %s' % (months, rep)
    return rep


########### Debug Helpers ###############
class Dbgtal:
    text = ""
    fakeUpdate = {'message':{'chat':{'id':'dbg'}}}
    def sendMessage(self,chat_id,text):
        self.text = text
    def answer(self):
        return self.text
    def returnFakeUpdate(self):
        return Struct(self.fakeUpdate)

class Struct:
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [Struct(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, Struct(b) if isinstance(b, dict) else b)
##########################################

##### Start Code #######
DebugObj = Dbgtal()
load_plugins()