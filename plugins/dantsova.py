#===isnttalismanplugin===
# -*- coding: utf-8 -*-

sys.path.append(os.path.join(os.path.abspath('.'), 'modules','DANTSOVA'))
from MarkoffLib import load_chain, make_acrotext

PLATFORM_PATH = os.path.join(u'modules',u'DANTSOVA', u'platform_build', u'dantsova.d0.plf')

# Correct alphabet of your language
CORRECT_ALPHABET = u'йцукенгшщзхъфывапролджэячсмитьбю'
import random
import json

from zipfile import *

def load_chain_zip(path):
    """

    """
    z = ZipFile(path+'.zip', 'r')

    chain = None
    fr = None
    try:
        fr = z.open(path.split('/')[-1])
        chain = json.load(fr)
    except:
        print "ERROR: " + str(sys.exc_info())
        return None
    finally:
        if fr != None:
            fr.close()
    z.close()
    return chain

platform = load_chain_zip(PLATFORM_PATH)

def handler_dantsova(source,parameters=''):
    input_text = (string.join(string.split(parameters)[1:])).encode('utf-8').decode('utf-8')
    #input_text = 'сообщение ушло'.decode('utf-8')
    random.seed(input_text)
    text = make_acrotext(platform, input_text, c=8, correct_alphabet=CORRECT_ALPHABET)
    #print text
    reply(source,text)



register_command_handler(handler_dantsova, 'донцова', ['инфо','мук','все'], 0, 'Алгоритм DANTSOVA', '', ['',''])
