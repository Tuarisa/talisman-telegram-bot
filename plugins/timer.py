#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  timer_plugin.py  

#  Initial Copyright © 2010 Tuarisa <Tuarisa@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import time

def handler_timer (source, parameters):
    if not parameters:
        reply(type, source, u'Эй, научись пользоваться ботом сначала!')
    str=0
    alarm = parameters.split()[0]
    if parameters.count (' '): str = parameters.split(' ', 1)[1]
    time.sleep(eval(alarm))
    if str:
        reply(source, str)
    else:
        reply(source, u'Проснись и пой!')
    
    
register_command_handler(handler_timer, 'таймер', ['инфо','фан','все'], 10, 'Отвечает через заданный промежуток времени заданным текстом.', 'таймер <время> <текст>', ['таймер 10*60 проснись и пой!'])