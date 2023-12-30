# Ctpbot

A script to find and react to !CTP commands in comments on the Hive blockchain.

*Please note that this software is in early Beta stage, and that you need to know what you are doing to use it.*

## Installation 

For Ubuntu and Debian install these packages:
```
sudo apt-get install python3-pip build-essential libssl-dev python3-dev python3-setuptools python3-gmpy2
```

### Install Python Packages

Install ctpbot by (you may need to replace pip3 by pip):
```
sudo pip3 install -U ctpbot beem hiveengine
```

## Configure And Run Ctpbot

First clone the Github repository to your home directory:
```
cd ~
git clone https://github.com/flaxz/ctpbot
```

After that edit your comment templates using Nano, there are 4 comment templates.
```
sudo apt install nano 
cd ~/ctpbot/templates
ls
nano COMMENT-TEMPLATE-1-2-3-4
```

Then edit your configuration file.
```
cd ~/ctpbot
nano ctpbot.config
```

Copy your configuration and comment templates to your working directory.
```
cd ~/ctpbot
sudo cp -R templates /usr/local/bin
sudo cp ctpbot /usr/local/bin
sudo cp ctpbot.config /usr/local/bin
sudo cp run-ctpbot.sh /usr/local/bin
```

Make the startup scripts executable.
```
cd /usr/local/bin
sudo chmod u+x ctpbot
sudo chmod u+x run-ctpbot.sh
```

Copy the Systemd config to it's directory.
```
cd ~/ctpbot
sudo cp ctpbot.service /etc/systemd/system
```

Reload Systemd and start the bot.
```
sudo systemctl daemon-reload
sudo systemctl start ctpbot.service
```

Get status and error messages.
```
sudo systemctl status ctpbot.service
q
```

Stop the bot.
```
sudo systemctl stop ctpbot.service
```

As has been stated above this bot is in early Beta and bugs and issues are likely to occur.

