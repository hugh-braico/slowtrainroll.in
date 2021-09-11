# 🎷 slowtrainroll.in

Skullgirls VOD site in the same vein as tunawithbacon.com, keeponrock.in, 
rockthedrag.in, etc

## What is this written in

* Web framework: Django 3.2
* Database: SQLite 
* Currently hosted on AWS Lightsail with Gunicorn

## How do the thing

- If you're not familiar with how Django works, read 
  [the tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)
- `pip3 install -r requirements.txt`
- generate a secret key and save it to a file called (yep) `/SECRET_KEY` 
  - see [Django deployment docs](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/#secret-key)
- set `DEBUG` in `slowtrainrollin/settings.py` to `True`
- `python3 manage.py migrate`
- `python3 manage.py runserver`

## Why is it called that?

Big Band says it during his 
[Take the A-Train](https://www.youtube.com/watch?v=cb2w2m1JmCY) special 
sometimes. I don't know if the voice line is a reference to anything specific.

The other name contender was hustlin.rocks since that is apparently a valid URL,
but since OCE is the Big Band region this one won out.
