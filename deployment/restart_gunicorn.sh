ps aux | grep gunicorn | grep slowtrainrollin | awk '{ print $2 }' | xargs kill -HUP
