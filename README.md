# 🎷 slowtrainroll.in

Skullgirls VOD site in the same vein as tunawithbacon.com, keeponrock.in, 
rockthedrag.in, etc

## What is this written in

* Web framework: Django 3.2
* Database: SQLite 
* Currently hosted on AWS Lightsail with gunicorn + nginx

## How do the thing

- If you're not familiar with how Django works, read 
  [the tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)
- `pip3 install -r requirements.txt`
- `sudo apt install node-less`
- generate a secret key and save it to a file called (yep) `/SECRET_KEY` 
  - see [Django deployment docs](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/#secret-key)
- set `DEBUG` in `slowtrainrollin/settings.py` to `True`
- `python3 manage.py migrate`
- `python3 manage.py runserver`

### Deploying with gunicorn+nginx

Use `python3 manage.py collectstatic` to collect all your static files
together to the `/static` directory where nginx can see them.

Install nginx and make sure you can see the default nginx page in browser

Set up nginx as a reverse proxy - basically use the .conf file from the
[Gunicorn deployment docs](https://docs.gunicorn.org/en/stable/deploy.html).

Start gunicorn as a background daemon and bind it to a Unix socket
(which nginx will attach to):

```bash
gunicorn -b unix:/tmp/gunicorn.sock --daemon slowtrainrollin.wsgi
```

Unlike the debug server you need to restart gunicorn after a git pull: 

```bash
ps aux | grep gunicorn | grep projectname | awk '{ print $2 }' | xargs kill -HUP
```

(You will also need to collectstatic again if any static files have changed)

Once HTTP looks good, use Let's Encrypt Certbot to generate SSL certs 
and then make sure it didn't do anything totally stupid to your 
nginx.conf in the process (spoiler: it did)

## Why is it called that?

Big Band says it during his 
[Take the A-Train](https://www.youtube.com/watch?v=cb2w2m1JmCY) special 
sometimes. I don't know if the voice line is a reference to anything specific.

The other name contender was hustlin.rocks since that is apparently a valid URL,
but since OCE is the Big Band region this one won out.
