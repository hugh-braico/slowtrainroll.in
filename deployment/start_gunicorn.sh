gunicorn \
-b unix:/tmp/gunicorn.sock \
--daemon slowtrainrollin.wsgi \
--log-file logs/gunicorn_logs 
