# Pittscord
A University of Pittsburgh Capstone Project Discord Bot

## Installation
### Unix
First, create a python virtual environment, e.g.:
```
python3 -m venv venv
```
Then, activate the venv
```
source venv/bin/activate
```
Next install the requirements
```
pip install -r requirements.txt
```

### Windows
Run
```
.\venv\Scripts\activate
```
in a Command Prompt

### Python venv use
As above, to activate the venv:
```
source venv/bin/activate
```
To deactivate:
```
deactivate
```

## Usage
The bot requires the following permissions:
- TODO ROUGH BELOW:

- ![image](https://github.com/neffers/Pittscord/assets/109564234/0d02a5f7-56ad-4ecb-bfad-a014fe03674a)

rough directions below:

minimum permissions link: https://discord.com/oauth2/authorize?client_id=1208123423763730434&permissions=309576715856&scope=bot

In order to work the bot:
Pre-anything else, click the link to add the bot to your server. The bot expects a "community server" with all those bells and whistles, which are (for some reason) required to have forum channels. It will make the rules channel visible and nothing else. It will create two roles (Previous Student and Previous TA) which will serve as 'default' roles, but will be assigned by the bot.
Proper bot rundown:
First, edit config.py to have abc123 as the admin.
Next, run the bot, either by executing the run_both.py or if you want to be able to run the web interface separate from the bot and have it work, ipc_server.py and in a separate terminal run web.py. If you don't need the web interface at all, you can simply run bot.py. Remember to be in a venv with the requirements installed.
Then, /reregister @yourself to and reply to the bot to register your id, and then /configure_server to perform initial setup.
A WARNING: /configure_server will alter the default role of the server, making most things not visible to a freshly joining user.
At that point, you should be able to use the web UI to perform management at-will.






### Configuration
In order to run the bot, there must be a `secret.py` containing the bot account's token.

See `secret.example.py`
