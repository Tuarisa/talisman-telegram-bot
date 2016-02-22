#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  trans_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Parts of code Copyright © Krishna Pattabiraman (PyTrans project) <http://code.google.com/p/pytrans/>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import urllib
import httplib

trans_langs={u'en': u'английский', u'ja': u'японский', u'ru': u'русский', u'auto': u'Определить язык', u'sq': u'албанский', u'en': u'английский', u'ar': u'арабский', u'af': u'африкаанс', u'be': u'белорусский', u'bg': u'болгарский', u'cy': u'валлийский', u'hu': u'венгерский', u'vi': u'вьетнамский', u'gl': u'галисийский', u'nl': u'голландский', u'el': u'греческий', u'da': u'датский', u'iw': u'иврит', u'yi': u'идиш', u'id': u'индонезийский', u'ga': u'ирландский', u'is': u'исландский', u'es': u'испанский', u'it': u'итальянский', u'ca': u'каталанский', u'zh-CN': u'китайский', u'ko': u'корейский', u'lv': u'латышский', u'lt': u'литовский', u'mk': u'македонский', u'ms': u'малайский', u'mt': u'мальтийский', u'de': u'немецкий', u'no': u'норвежский', u'fa': u'персидский', u'pl': u'польский', u'pt': u'португальский', u'ro': u'румынский', u'ru': u'русский', u'sr': u'сербский', u'sk': u'словацкий', u'sl': u'словенский', u'sw': u'суахили', u'tl': u'тагальский', u'th': u'тайский', u'tr': u'турецкий', u'uk': u'украинский', u'fi': u'финский', u'fr': u'французский', u'hi': u'хинди', u'hr': u'хорватский', u'cs': u'чешский', u'sv': u'шведский', u'et': u'эстонский', u'ja': u'японский'}
yandex_key="trnsl.1.1.20160221T204840Z.47263b919c6d8a98.755cc786f3a513856ad3a57286b9842d2689363f"

def handler_google_trans(source,parameters):
    param=parameters.split(None, 2)
    if param[0] in trans_langs.keys() and param[1] in trans_langs.keys() and len(param)>=3:
        (fl, tl, text)=param
        if fl=='auto':
            if tl=='auto':
                reply(source, u'ошибочный запрос. прочитай помощь по использованию команды')
                return
            else:
                answ=google_detect_lang(text)
                if answ in trans_langs.keys():
                    fl=answ
                else:
                    reply(source, answ)
                    return
        answ=google_translate(text, fl, tl)
        answ=answ.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        reply(source,answ)
    else:
        reply(source, u'ошибочный запрос. прочитай помощь по использованию команды')

def handler_yandex_trans(source,parameters):
    param=parameters.split(None, 2)
    if (param[0] in trans_langs.keys() and param[1] not in trans_langs.keys()):
        param = ['auto'] + ' '.join(param).split(None,1)
    if param[0] in trans_langs.keys() and param[1] in trans_langs.keys() and len(param)>=3:
        (fl, tl, text)=param
        if fl=='auto':
            if tl=='auto':
                reply(source, u'ошибочный запрос. прочитай помощь по использованию команды')
                return
            else:
                answ=yandex_detect_lang(text)
                if answ in trans_langs.keys():
                    fl=answ
                else:
                    reply(source, answ)
                    return
        answ=yandex_translate(text, fl, tl)
        answ=answ.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        reply(source,answ)
    else:
        reply(source, u'ошибочный запрос. прочитай помощь по использованию команды')

def google_translate(text, from_lang, to_lang):
    try:
        req = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%s&langpair=%s%s' % (urllib2.quote(text.encode('utf-8')), from_lang+'%7C', to_lang))
    except urllib2.HTTPError, e:
        return str(e)
    answ=json.load(req)
    if answ['responseStatus']!=200:
        return str(answ['responseStatus'])+': '+answ['responseDetails']
    elif answ['responseData']:
        return answ['responseData']['translatedText']
    else:
        return u'неизвестная ошибка'

def google_detect_lang(text):
    try:
        req = urllib2.urlopen('http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&q=' + urllib2.quote(text.encode('utf-8')))
    except urllib2.HTTPError, e:
        return str(e)
    answ=json.load(req)
    if answ['responseStatus']!=200:
        return str(answ['responseStatus'])+': '+answ['responseDetails']
    elif answ['responseData']:
        return answ['responseData']['language']
    else:
        return u'неизвестная ошибка'

def yandex_detect_lang(text):
    try:
        req = urllib2.urlopen('https://translate.yandex.net/api/v1.5/tr.json/detect?key='+yandex_key+'&text=' + urllib2.quote(text.encode('utf-8')))
    except urllib2.HTTPError, e:
        return str(e)
    answ=json.load(req)
    if answ['code']!=200:
        return str(answ)
    elif answ['code']==200:
        return answ['lang']
    else:
        return u'неизвестная ошибка'

def yandex_translate(text, from_lang, to_lang):
    try:
        req = urllib2.urlopen('https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&lang=%s%s&text=%s' % (yandex_key, from_lang+'-', to_lang, urllib2.quote(text.encode('utf-8'))))
    except urllib2.HTTPError, e:
        return str(e)
    answ=json.load(req)
    if answ['code']!=200:
        return str(answ)
    elif answ['code']==200:
        return answ['text'][0]
    else:
        return u'неизвестная ошибка'


try:
    import json
    register_command_handler(handler_yandex_trans, 'перевод', ['инфо','все'], 10, 'Перевод с одного языка в другой. Используется Google Translate. Доступные для перевода языки:\n' + ', '.join(sorted([x.encode('utf-8')+': '+y.encode('utf-8') for x,y in trans_langs.iteritems()])), 'перевод <исходный_язык> <нужный_язык> <фраза>', ['перевод en ru hello', 'перевод ru en привет'])
except ImportError:
    try:
        import simplejson as json
        register_command_handler(handler_yandex_trans, 'перевод', ['инфо','все'], 10, 'Перевод с одного языка в другой. Используется Google Translate. Доступные для перевода языки:\n' + ', '.join(sorted([x.encode('utf-8')+': '+y.encode('utf-8') for x,y in trans_langs.iteritems()])), 'перевод <исходный_язык> <нужный_язык> <фраза>', ['перевод en ru hello', 'перевод ru en привет'])
    except:
        print '====================================================\nYou need Python 2.6.x or simple_json package installed to use trans_plugin.py!!!\n====================================================\n'
