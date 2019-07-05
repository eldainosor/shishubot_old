# shishu_bot
A python-telegram-bot that can be used to get OTA info for BootleggersROM.

Runs on telegram as [shishu_bot](https://t.me/shishu_ota_bot).

## Starting the bot.

Once you've setup your configuration (see below) is complete, simply run:

`python3 -m shishu_bot`

### Configuration

There are two possible ways of configuring your bot: a config.py file, or ENV variables.

The prefered version is to use a `config.py` file, as it makes it easier to see all your settings grouped together.
This file should be placed in your `shishu_bot` folder, alongside the `__main__.py` file . 
This is where your bot token will be loaded from.

An example `config.py` file could be:
```
class Config:
    API_KEY = "your bot api key"  # your api key, as provided by the botfather    
```

If you can't have a config.py file (EG on heroku), it is also possible to use environment variables.
The following env variables are supported:
 - `ENV`: Setting this to ANYTHING will enable env variables
 - `TOKEN`: Your bot token, as a string.

### Python dependencies

Install the necessary python dependencies by moving to the project root directory and running:

`sudo pip3 install -r requirements.txt`.

This will install all necessary python packages.

Have Fun!
