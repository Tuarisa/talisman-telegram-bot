#===istalismanplugin===
# -*- coding: utf-8 -*-

def handler_ping(source,params=''):
    reply(source,"понг")

def handler_sarcasm(source,params):
    reply(source,"http://images.derstandard.at/2014/06/05/sarcasm.jpg")

def handler_git(source,params):
    if (params.strip()==u'боль'):
        reply(source,"Доооо")
    elif (params.strip()==u'няшка'):
        reply(source,"Ага")

register_command_handler(handler_ping, 'пинг', ['инфо','мук','все'], 0, 'Пингует тебя или определённый ник или сервер.', 'пинг [ник]', ['пинг guy','пинг jabber.aq'])
register_command_handler(handler_sarcasm, 'сарказм', ['инфо','мук','все'], 0, 'Самая важная команда', 'сарказм', ['сарказм','пинг'])
register_command_handler(handler_git, 'гит', ['инфо','мук','все'], 0, 'Самая важная команда', 'сарказм', ['сарказм','пинг'])

