#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  weather_plugin.py    

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploru.net>
#  Modifications Copyright © 2010 Tuarisa <Tuarisa@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import pymetar

WEATHERCODE_FILE = 'static/weather.txt'


def handler_weather_weather(source, parameters):
    if not parameters:
        reply(source, u'ииии?')
        return
    try:
        rf=pymetar.ReportFetcher(parameters.strip())
        fr=rf.FetchReport()
    except Exception, ex:
        if parameters.count('/'):
            parameters = return_code(parameters.rsplit(' ', 1)[0]).split()[int(parameters.split('/')[1])-1]
        else:
            parameters = return_code(parameters).split()[0]
        try:
            rf=pymetar.ReportFetcher(parameters.strip())
            fr=rf.FetchReport() 
        except Exception, ex:
#           reply(type, source, u'А оно есть?')
            return  
    rp=pymetar.ReportParser()
    pr=rp.ParseReport(fr)
    tm=time.strptime(pr.getISOTime(), '%Y-%m-%d %H:%M:%SZ')
    tm=time.mktime(tm)
    tmn=time.mktime(time.gmtime())
    tm=tmn-tm
    tm=timeElapsed(tm)
    rep = u'погода в %s (%s) %s назад\n%s, температура: %s° C, влажность: %s%%, ' %(pr.getStationName(), parameters.strip(), tm, pr.getWeather(), pr.getTemperatureCelsius(), pr.getHumidity())
    if pr.getWindSpeed():
        rep+=u'ветер: %s м/с, ' %(int(round(pr.getWindSpeed())))
    if pr.getPressure():
        press = pr.getPressure()
        press  = 0.7500616 * press
        pres = int(round(press))
        rep+=u'давление: %s мм.рт.ст., ' %(pres)
    rep+=u'облачность: %s' %(pr.getSkyConditions())
    reply(source, rep)
    station = pr.getStationName()
    temp = return_code(parameters)
    if (temp == u'хз'):
        f=open(WEATHERCODE_FILE, 'a')
        f.write('%s => %s\n' %(parameters, station))
        f.close()

def return_code(parameters):
    if not parameters:
        return (u'чё-то ты не то написал...')
    if len(parameters)<=2:
        return (u'какая-то фигня...')
    results = ''
    query = string.lower(parameters)
    fp = open(WEATHERCODE_FILE, 'r')
    lines = fp.readlines()
    for line in lines:
        line = line.decode('utf8').replace('\n',' \n')
        if string.count(string.lower(line), query):
            results += string.split(line, u'=> ')[0]
    if results:
        return (results)
    else:
        return (u'я не знаю города ' +query)


def handler_weather_weathercode(source, parameters):
        reply(source, return_code(parameters))
        return
        
def handler_weather_plus(source, parameters):
    if not parameters:
        return (u'ну и чё?')
    code = return_code(parameters)
    for c in code.split(' '):
        if (c==''):
            return
        else:
            handler_weather_weather(source, c)
    return


register_command_handler(handler_weather_weather, 'погода', ['инфо','все'], 10, 'Смотрит погоду из NOAA, или по названию города, или погоду в определённом по счёту аэропорту', 'погода <4буквенный_код_города>', ['погода ukhh', 'погода moscow', 'погода москва /1'])
register_command_handler(handler_weather_plus , 'погода+', ['инфо','все'], 10, 'Смотрит погоду в городе N во всех аэропортах', 'погода+ <город>', ['погода+ moscow'])
register_command_handler(handler_weather_weathercode, 'код', ['инфо','все'], 10, 'Показывает код города для просмотра погоды', 'код <город>', ['код orel'])
