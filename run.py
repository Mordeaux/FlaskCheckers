#!/usr/bin/python

from flask import Flask
from FlaskCheckers import checkers

app = Flask(__name__)
app.register_blueprint(checkers)

if __name__ == '__main__':
    app.run(debug=True)

