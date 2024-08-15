# Word by Word – flashcards

## How to use

Consider to create a [venv](https://docs.python.org/3/library/venv.html).

In the *main* folder set a symlink to *settings.dev* (or to *.prod* on production).
For production use create a .env file with a row like `export PROD_URL="some.url"`.

Then:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_tables
python manage.py runserver 0.0.0.0:8001 --insecure
#                                        ^
# Whilst this flag does work, it does not serve the content from the collectstatic folder
```
https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail

In another terminal:
```
nvm use 18.14.1
npm install

npm run dev
or
npm run build
```
This "npm run build" is for production use, the resulted files will not follow local frontend changes.

Visit `http://localhost:8001`

Visit `http://localhost:8001/2`

Visit `http://localhost:8001/3`

Use the upper right gray "Reset" ("Alaphelyzetbe") button to sync localstorage to backend output.
(Until you don't push this button, the unknown expressions appear at the end of every swipe loop.)

This project was made basically for Phone displayed Hungarian / Other language cards, but this can be changed. You can click on cards to show the other language, and swipe left (unknown) or right (known) to make a card disappear.

![kép](https://github.com/user-attachments/assets/6a78aef8-885e-4640-83aa-921c0c247407)
