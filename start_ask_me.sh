#!/bin/bash
cd ~/github/Web/ask_me
sudo service nginx start
gunicorn ask_me.wsgi -b 127.0.0.1:8081
exit 0
