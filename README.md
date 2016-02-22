# talisman-telegram-bot

Talisman Telegram Bot

His father is Talisman XMPP Multiuser Conference bot. It has the same plugin system and ideology. Simple for quick start with Telegram bots.

It works with FLASK, Google App Engine and Python Telegram Bot.

Becouse this is not standart python libraries, you need to install Google App Engine tools (command line tools, first of all), Flask and Python Telegram bot. 

For deploy this app to GAE, you need to use venv. 

Choise your project directory and run following commands:

pip install virtualenv


virtualenv venv


. venv/bin/activate


pip install Flask


pip install python-telegram-bot


pip install signal


deactivate

Before you run your app, get token for Telegram Bot (@botfather) and Google App Engine App ID, then create copy of file config-sample.txt, name it config.txt, fill your token and URL.

To start your app locally write:

dev_appserver.py talismant (where talismant is your app folder)

To deploy your app to GAE write:

appcfg.py -A talismant-**** update talismant (where talismant-**** is your GAE app id)