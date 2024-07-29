# Demo Project

## How to use

Consider to create a [venv](https://docs.python.org/3/library/venv.html).

In the *main* folder set a symlink to *settings.dev* (or to *.prod* on production).

Then:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 --insecure
#                                        ^
# Whilst this flag does work, it does not serve the content from the collectstatic folder
# https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail
```

In Another terminal
```
nvm use 18.14.1
npm install

npm run dev
or
npm run build
```
(This ...build is for production use, it will not follow frontend changes.)

Visit `http://localhost:8000`

