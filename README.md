# Telegram server control panel
---
### Description:
The project provides easy way to control your server based on GNU/Linux. You may control your services (based on systemctl command). Project is fully has open-source code and provided with MIT license, for more details, see [license file](https://github.com/Vicrorege/tg-server-cp/blob/master/LICENSE).
### Installation
> IMPORTANT! All the steps below runs from root user
1. Firstly, you need to get the API token of your future bot via [BotFather](https://t.me/BotFather), follow the instruction below:
![instruction](https://raw.githubusercontent.com/Vicrorege/tg-server-cp/refs/heads/master/readme/botfather_guide.png)
2. Download the project from GitHub.
```
git clone "https://github.com/Vicrorege/tg-server-cp"
cd tg-server-cp
```
3. Make installer executable and run it. Installer will build the python virtual environment, download required libraries and create the service, named <b>tgcp</b>
```
chmod +x installer.sh
./install.sh
```
Installer will automatically open nano two times: firstly, will open .service file, where you need to edit path of the project:
```
[Unit]
Description=tgcp

[Service]
User=root
Group=root
Type=simple
ExecStart=/root/tg-server-cp/venv/bin/python3/root/ tg-server-cp/main.py # place to edit the path
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Secondly, will open config.json, where you need to paste your API token, and choose the language.
```
{
    "bot_token": "", // place for your API Token
    "allowed_users": [
        
    ],
    "app": {
        "lang": "en" // place for your language (ru, en)

    },
    "services": [

    ]
}
```

4. After successful installation, send /start to your bot. Bot will give you your id, which you need to paste in your config.json
```
nano config.json
systemctl restart tgcp
```
, like
```
"allowed_users": [
    12345678 // your id
]
```
you may also add to service, to manage it with your bot.
```
"services": [
    "site" // your services
]
```