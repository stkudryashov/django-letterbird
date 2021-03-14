# django-letterbird
**Anonymous messaging service**

****

1. From `requirements.txt` install all requirements
2. Create `mystery.py` file in a directory with `manage.py`
3. Past in `mystery.py` your secrets keys:

`SECRET_KEY = 'your secret key from Django'`

`RECAPTCHA_PUBLIC_KEY = 'your captcha key'`

`RECAPTCHA_PRIVATE_KEY = 'your captcha key'`

****

4. `python manage.py migrate`
5. `python manage.py collectstatic`
