Flask Checkers
==============

By Michael Mordowanec

http://github.com/Mordeaux

http://mordowanec.com

Getting Started
===============
First clone the repository.
```
git clone https://github.com/Mordeaux/Flask_Checkers.git
```
Install Flask
```
pip install flask
```
You should now be able to run the app on your local machine with:
```
./run.py
```
Alternatively, you could install it as a Flask Blueprint in any Flask application you have running. Simply add this snippet of code to your app:
```python
from flask import register_blueprint
import sys
sys.path.insert(0, '/full/path/to/repository')
from FlaskCheckers import checkers
```
Then after your app is created in the script you simply register the Blueprint.
```python
app.register_blueprint(checkers, url_prefix='/checkers')
```

Contributing
============

Feel free to fork this project and suggest changes, there are a million ways it could be improved yet. I will try to keep the most current version running here:

http://mordowanec.com/checkers

