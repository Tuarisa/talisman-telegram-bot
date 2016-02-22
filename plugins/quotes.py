#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  quotes_plugin.py

#  Initial Copyright © ???
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import urllib2,re,urllib

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')

def handler_bashorgru_get(source, parameters):
    if parameters.strip()=='':
        req = urllib2.Request('http://bash.im/forweb/?u')
        req.add_header = ('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    else:
        req = urllib2.Request('http://bash.im/quote/'+parameters.strip())
        req.add_header = ('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    r = urllib2.urlopen(req)
    target = r.read()
    print target
    #"""link to the quote"""
    od = re.search('<a href="/quote/',target)
    print od
    b1 = target[od.end():]
    print b1
    b1 = b1[:re.search('/rulez" class="up"',b1).start()]
    print b1
    b1 = strip_tags.sub('', b1.replace('\n', ''))
    print b1
    b1 = 'http://bash.im/quote/'+b1+'\n'
    #"""quote"""
    print b1
    od = re.search(r'<div class="quote">.*?<div class="actions">.*?</div>.*?<div class="text">(.*?)</div>.*?</div>', target, re.DOTALL)
    message = b1+od.group(1)
    message = decode(message)
    message = '\n' + message.strip()
    reply(source,unicode(message,'windows-1251'))

        
        
def handler_bashorgru_abyss_get(source, parameters):
    if parameters.strip()=='':
        req = urllib2.Request('http://bash.im/abysstop')
    else:
        reply(source,u'бездна не поддерживает номера')
        return
    req.add_header = ('User-agent', 'Mozilla/5.0')
    try:
        r = urllib2.urlopen(req)
        target = r.read()
        id=str(random.randrange(1, 25))
        """start"""
        od = re.search('<b>'+id+':',target)
        q1 = target[od.end():]
        q1 = q1[:re.search('\n</div>',q1).start()]
        """quote"""
        od = re.search('<div>',q1)
        message = q1[od.end():]
        message = message[:re.search('</div>',message).start()]          
        message = decode(message)
        message = '\n' + message.strip()
        reply(source,unicode(message,'windows-1251'))
    except:
        reply(source,u'аблом какой-то')        

def decode(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')

register_command_handler(handler_bashorgru_get, 'бор', ['фан','инфо','все'], 0, 'Показывает случайную цитату из бора (bash.org.ru). Также может по заданному номеру вывести.', 'бор', ['бор 223344','бор'])
register_command_handler(handler_bashorgru_abyss_get, 'борб', ['фан','инфо','все'], 0, 'Показывает случпйную цитату из бездны бора (bash.org.ru).', 'борб', ['борб'])
