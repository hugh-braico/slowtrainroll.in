# 🎷 slowtrainroll.in

https://slowtrainroll.in/

Skullgirls VOD site in the same vein as tunawithbacon.com, keeponrock.in, 
rockthedrag.in, etc

## What is this written in

* Web framework: Django 3.2
* Database: SQLite
* Most code written in python
* Hosted on AWS Lightsail with gunicorn + nginx

## Getting started

### Requirements

- Unix-like environment
- Python 3.6+
- `nodejs` + `npm`

### Development setup

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install the CSS precompiler
sudo npm install less -g

# Generate and save a secret key
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' > SECRET_KEY

# (Dev only) set a flag to run the dev server in debug mode
export STR_DEBUG=True

# Apply migrations to the database
python3 manage.py migrate

# Run the dev server
python3 manage.py runserver
```

Connect to http://127.0.0.1:8000/ in your browser to check it works.

To test the admin backend, `python3 manage.py createsuperuser` then visit 
http://127.0.0.1:8000/admin in your browser.

### Deploying with gunicorn+nginx

Use `python3 manage.py collectstatic` to collect all your static files together
to the `/static` directory where nginx can see them.

Install nginx and make sure you can see the default nginx page in browser.

Set up nginx as a reverse proxy - basically use the .conf file from the
[Gunicorn deployment docs](https://docs.gunicorn.org/en/stable/deploy.html).
There is an example in the `deployment/` folder that you can adapt.

Start gunicorn as a background daemon and bind it to a Unix socket
(which nginx will attach to):

```bash
bash deployment/start_gunicorn.sh
```

Once HTTP looks good, use [Let's Encrypt](https://certbot.eff.org/) to 
generate SSL certs and then make sure it didn't mess up your nginx.conf

### Applying updates to prod after initial deployment

SSH into the prod server:

```bash
# pull down changes from git
git pull

# apply migrations if any models have changed
python3 manage.py migrate

# collect any changes to static files if any were changed
python3 manage.py collectstatic

# restart server
bash deployment/restart_gunicorn.sh
```

### Adding and exporting data

This is a little unsophisticated but I don't see the database growing past
about 10MB (<1MB currently), so it can afford to be.

The [admin backend](https://slowtrainroll.in/admin/admin/csvuploadpage/) has
a page to add vods, and also bulk-upload vods via 
[TWB-style csv files](https://github.com/Servan42/TWB_Parser).

The [/backup.csv](https://slowtrainroll.in/backup.csv) page presents every vod
in plaintext TWB csv format.

## Why the name slowtrainroll.in?

Big Band says it during his 
[Take the A-Train](https://www.youtube.com/watch?v=cb2w2m1JmCY) special, and
it's a reference to the blues song
[Train Kept A-Rollin'](https://en.wikipedia.org/wiki/Train_Kept_A-Rollin%27)
by Tiny Bradshaw.

The other name contender was
[hustlin.rocks](https://wiki.gbl.gg/w/Skullgirls/Cerebella#Supers) since that
is apparently a valid URL, but since OCE is the Big Band region this one won
out.
