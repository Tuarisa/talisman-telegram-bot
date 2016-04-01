#===istalismanplugin===
# -*- coding: utf-8 -*-


def handler_admin_say(source, parameters):
    if parameters:
        args=parameters.split()[0]
        reply(source, parameters)
    else:
        reply(source, u'ошибочный запрос. прочитай помощь по использованию команды')

def handler_admin_msg(source, parameters):
    if not parameters:
        reply(source, u'ошибочный запрос. прочитай помощь по использованию команды')
        return
    msg(string.split(parameters)[0], string.join(string.split(parameters)[1:]))
    reply(source, u'сообщение ушло')

def handler_admin_myid(source, parameters):
    reply(source, source.message.chat_id)
    

register_command_handler(handler_admin_say, 'сказать', ['админ','мук','все'], 20, 'Говорить через бота в конференции.', 'сказать <сообщение>', ['сказать салют пиплы'])
register_command_handler(handler_admin_msg, 'мессага', ['админ','мук','все'], 40, 'Отправляет сообщение от имени бота на определённый JID.', 'мессага <jid> <сообщение>', ['мессага guy@jabber.aq здорово чувак!'])
register_command_handler(handler_admin_myid, 'мойид', ['админ','мук','все'], 40, '', '', [''])
