#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  horoscope_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import xml.dom.minidom

horo_cache={}

horodb={u'овен': u'aries', u'телец': u'taurus', u'близнецы': u'gemini', u'рак': u'cancer', u'лев': u'leo', u'дева': u'virgo', u'весы': u'libra', u'скорпион': u'scorpio', u'стрелец': u'sagittarius', u'козерог': u'capricorn', u'водолей': u'aquarius', u'рыбы': u'pisces'}
whendb={u'вчера': u'yesterday', u'сегодня': u'today', u'завтра': u'tomorrow', u'послезавтра': u'tomorrow02'}

def horo_update_cache():
    try:
        req=urllib2.urlopen('http://img.ignio.com/r/export/utf/xml/daily/com.xml')
    except urllib2.HTTPError, e:
        if e.code==404:
            reply(type,source,u'кто это?')
            return
        else:
            reply(type,source,str(e))
            return
    horo_parse_horo(xml.dom.minidom.parse(req))

def horo_parse_horo(raw_horo):
    horo_cache.clear()
    for sign in raw_horo.firstChild.childNodes:
        sign=sign.nodeName
        if sign in horodb.itervalues():
            horo_cache[sign]={}
    raw_date=raw_horo.getElementsByTagName("date")[0]
    horo_cache['date']={'yesterday': raw_date.getAttribute('yesterday'), 'today': raw_date.getAttribute('today'), 'tomorrow': raw_date.getAttribute('tomorrow'), 'tomorrow02': raw_date.getAttribute('tomorrow02')}
    for sign in horodb.itervalues():
        raw_sign=raw_horo.getElementsByTagName(sign)[0].childNodes
        for day in xrange(1,8,2):
            horo_cache[sign][raw_sign[day].nodeName]=raw_sign[day].firstChild.data.strip()
    print u'horoscope updated: '+time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime())
    #threading.Timer(3600, horo_update_cache).start()


def handler_horo_igniocom(source, parameters):
    if not parameters:
        reply(source, u'ошибочный запрос. прочитай помощь по использованию команды')
    else:
        temp,sign,when=parameters.strip().split(),'',''
        if len(temp)==1:
            sign=parameters
            when=u'today'
        elif len(temp)>1:
            (sign, when)=temp[0:2]
            if not when in whendb.keys():
                reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
                return
            when=whendb[when]
        if sign.strip() in horodb.keys():
            try:
                reply(source, horo_cache[horodb[sign.strip()]][when])
            except:
                reply(source, u'в данный момент происходит обновление гороскопа. повторите ваш запрос позже')
                horo_update_cache()
        else:
            print [sign]
            reply(source, u'ошибочный запрос. прочитай помощь по использованию команды')


def handler_horo_update(source, parameters):
    horo_update_cache()

register_command_handler(handler_horo_igniocom, 'гороскоп', ['инфо','фан','все'], 0, 'Показывает гороскоп для указаного знака гороскопа. Возможен просмотр гороскопа за определённый день - вчера, сегодня (по умолчанию), завтра и послезавтра. Доступные знаки: '+', '.join([x.encode('utf-8') for x in horodb.keys()]), 'гороскоп [знак] <когда>', ['гороскоп козерог','гороскоп рыбы вчера'])
register_command_handler(handler_horo_update, 'гороскопапдейт', ['инфо','фан','все'], 0, 'Апдейт гороскопа', 'гороскопапдейт', ['гороскопапдейт'])

#register_stage2_init(horo_update_cache)
