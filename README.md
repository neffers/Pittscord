# Pittscord
A University of Pittsburgh Capstone Project Discord Bot

## Installation
First, create a python virtual environment, e.g.:
```
python3 -m venv venv
```
Then, activate the venv
### Unix and Mac
```
source venv/bin/activate
```
### Windows
```
.\venv\Scripts\activate
```
Next install the requirements (the same across platforms)
```
pip install -r requirements.txt
```

### Configuration
In order to run the bot, there must be a `secret.py` containing the bot account's token, as well as your Canvas token.
The Discord token in `secret.py` must be edited/updated when creating a new bot account.
See `secret.example.py` for an example of what is expected.

There is also a `config.py` file where you can change some settings.
See the file for more details.

## Usage
If you wish to use the preexisting "Pittscord" bot, simply use this bot
[invitation link](https://discord.com/oauth2/authorize?client_id=1208123423763730434&permissions=311724199504&scope=bot).
This requires that you have our bot token to run, however.
If you wish to create your own, new bot account, see the section titled [Bot Creation](#bot-creation)

The bot expects a "Community Server", as it expects there to be a 'rules' channel.
It also expects to be able to create forum channels and will probably crash if it tries and can't.

In order to work the bot:
1. Remember to be in a venv with the requirements installed.
2. Run the bot, either by executing the run_both.py or if you want to be able to run the web interface separate from the bot, ipc_server.py and in a separate terminal run web.py.
   If you don't need the web interface at all, you can simply run bot.py.
3. Use the `/register` command to register yourself and reply to the bot to register your id.
4. Use the `/configure_server` command to perform initial setup.
   **WARNING: /configure_server will alter the default role of the server, making most things not visible to a freshly joining user.**
   However, you can change those visibility settings at your leisure.
   It will also create two roles (Previous Student and Previous TA) which will serve as 'default' roles, but will be assigned by the bot.
   You can also freely rename these roles and assign them whatever cosmetic changes suit you.

Once you've done the above, you should be able to use the web UI to perform management at-will.

### Available Commands
#### Administrator Only
- `/configure_server`
   - Intended for a one-time use to configure the server for usage.
- `/identify @user`
   - Provides the pitt id associated with the user's account.
- `/reregister @user`
   - Pretends that the user just joined the server, asking for a pittid and assigning to classes if available.
- `/reregister_all`
   - As above, performed on all accounts in the server. Will probably send a message to every user in the server.
- `/deregister @user`
   - Removes a user's pitt id from the database
#### Available to all users
- `/register`
   - Allows a user to simulate re-joining the server (to try to register with the bot for a new class, for example)

## Warnings / Be aware
If a bot-created role is ever moved above the role of the Discord bot, in terms of Discord roles and their priority, it will no longer have permissions to edit that role. So, make sure you do not.
If a permission is added to a student/TA role that the Discord bot does not have, the Discord bot will no longer be able to handle those roles administratively.

## Bot Creation
These are the minimum permissions required for the Discord bot to run properly:

### General Permissions
* Manage Roles
* Manage Channels
* Change Nickname
* Read Messages/View Channels

### Text Permissions
* Send Messages
* Create Public Threads
* Send Messages in Threads
* Embed Links
* Attach Files
* Read Message History
* Use External Emojis
* Add Reactions
* Use Slash Commands

### Voice Permissions
* Connect
* Speak
* Video

![image](./images/botPermissionsChecklist.png)

### Creating your own bot
1. Ensure that your account has access to the Discord Development Portal.
2. Create a "New Application" and check that "Guild Install" is selected.
3. On the "OAuth2" tab, click "bot" and select the minimum permissions needed.
   (You could also simply select `Administrator` which grants the bot root effectively root access to the server.)
4. Enter the generated URL, and select the server you wish for your bot to run in.

Congrats! Your bot should have joined the server
