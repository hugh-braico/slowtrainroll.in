# 🎷 slowtrainroll.in

Skullgirls VOD site in the same vein as tunawithbacon.com, keeponrock.in, 
rockthedrag.in, etc

## What is this written in

* Web framework: Django 3.2
* Database: SQLite 
* [Currently hosted](https://slowtrainroll.in/) on AWS Lightsail with 
  gunicorn + nginx

## How do the thing

### Requirements

- Unix-like environment (I use WSL2 Ubuntu)
- Python 3.6+
- `nodejs` and `npm`
- [A working knowledge of Django](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)

### Development setup

After cloning the repo and entering the directory:

- Install Python dependencies: `pip3 install -r requirements.txt`
- Install the CSS precompiler: `sudo npm install less -g`
- Generate and save a secret key: `python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' > SECRET_KEY` 
  - see [Django deployment docs](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/#secret-key)
- (Dev only) set a flag to run the dev server in debug mode: `export STR_DEBUG=True`  
- Apply migrations to the database: `python3 manage.py migrate`
- Run the dev server: `python3 manage.py runserver`
- Connect to http://127.0.0.1:8000/ in your browser to check it works
- To test the admin backend, `python3 manage.py createsuperuser` then
  visit http://127.0.0.1:8000/admin in your browser

### Deploying with gunicorn+nginx

Use `python3 manage.py collectstatic` to collect all your static files together
to the `/static` directory where nginx can see them.

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
ps aux | grep gunicorn | grep slowtrainrollin | awk '{ print $2 }' | xargs kill -HUP
```

(You will also need to collectstatic again if any static files have changed)

Once HTTP looks good, use [Let's Encrypt Certbot](https://certbot.eff.org/) to 
generate SSL certs and then make sure it didn't do anything totally stupid to 
your nginx.conf in the process (spoiler: it did)

## Why is it called that?

Big Band says it during his 
[Take the A-Train](https://www.youtube.com/watch?v=cb2w2m1JmCY) special 
sometimes. I don't know if the voice line is a reference to anything specific.

The other name contender was hustlin.rocks since that is apparently a valid URL,
but since OCE is the Big Band region this one won out.
